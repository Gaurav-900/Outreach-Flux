import os
import asyncio
from typing import List
import json
from datetime import datetime, timezone

from app.core.supabase import supabase
from app.core.config import get_candidate_profile
from app.providers.llm import CompanyContext, GeminiAdapter, DeepSeekAdapter, EmailDraft

class OutreachGeneratorService:
    def __init__(self):
        self.gemini = GeminiAdapter()
        self.deepseek = DeepSeekAdapter()
        # Fallback batch size to 4 if env var is missing or invalid
        try:
            self.batch_size = int(os.getenv("EMAIL_BATCH_SIZE", "4"))
        except ValueError:
            self.batch_size = 4

    async def generate_batch(self) -> int:
        print(f"[OutreachGenerator] Starting generation batch. Max size: {self.batch_size}")
        
        # 1. Fetch READY_FOR_OUTREACH companies that don't have drafts yet
        res = supabase.table('companies').select('*').eq('outreach_status', 'READY_FOR_OUTREACH').limit(self.batch_size).execute()
        companies = res.data
        
        if not companies:
            return 0

        print(f"[OutreachGenerator] Found {len(companies)} companies ready for outreach.")
        
        # 2. Prepare Contexts
        candidate_profile = get_candidate_profile()
        candidate_text = candidate_profile.model_dump_json(exclude_none=True)

        # Assuming DiscoveryPreferences holds target location
        profile_data = candidate_profile.model_dump(exclude_unset=True)
        prefs = profile_data.get('discovery_preferences') or {}
        locations = prefs.get('preferred_locations') or []
        location_pref_str = ", ".join(locations) if locations else None

        contexts: List[CompanyContext] = []
        valid_companies = []

        for company in companies:
            # Check if outreach already exists to prevent duplicate generation
            existing = supabase.table('outreach').select('id').eq('company_id', company['id']).execute()
            if existing.data:
                print(f"[OutreachGenerator] Draft already exists for company {company['id']}. Skipping.")
                continue
            
            # Fetch research content
            research_res = supabase.table('company_research').select('content').eq('company_id', company['id']).execute()
            research_content = research_res.data[0]['content'] if research_res.data else None

            # Look for contact separately
            contact_res = supabase.table('contacts').select('*').eq('company_id', company['id']).limit(1).execute()
            contact = contact_res.data[0] if contact_res.data else None
            
            ctx = CompanyContext(
                company_id=company['id'],
                company_name=company.get('name', 'Unknown Company'),
                research_content=research_content,
                contact_name=contact.get('name') if contact else None,
                contact_role=contact.get('role') if contact else None,
                candidate_profile=candidate_text,
                location_preference=location_pref_str
            )
            contexts.append(ctx)
            valid_companies.append({
                'company_id': company['id'],
                'contact_id': contact['id'] if contact else None
            })

        if not contexts:
            return 0

        # 3. Call LLM Provider with retry & fallback logic
        drafts: List[EmailDraft] = []
        
        # Try Gemini first
        if self.gemini.is_available():
            print("[OutreachGenerator] Attempting Gemini (1st try)...")
            drafts = await self.gemini.generate_drafts(contexts)
            if not drafts:
                print("[OutreachGenerator] Gemini 1st try failed. Waiting 15 seconds...")
                await asyncio.sleep(15)
                print("[OutreachGenerator] Attempting Gemini (2nd try)...")
                drafts = await self.gemini.generate_drafts(contexts)

        # Fallback to DeepSeek
        if not drafts and self.deepseek.is_available():
            print("[OutreachGenerator] Gemini failed or unavailable. Falling back to DeepSeek...")
            drafts = await self.deepseek.generate_drafts(contexts)

        if not drafts:
            print("[OutreachGenerator] All LLM generation attempts failed. Marking batch as GENERATION_FAILED.")
            for comp_meta in valid_companies:
                try:
                    supabase.table('companies').update({
                        'outreach_status': 'GENERATION_FAILED'
                    }).eq('id', comp_meta['company_id']).execute()
                except Exception as e:
                    print(f"Failed to update status for {comp_meta['company_id']}: {e}")
            return 0

        print(f"[OutreachGenerator] Successfully generated {len(drafts)} drafts.")

        # 4. Save Drafts & Update Status
        draft_dict = {d.company_id: d for d in drafts}

        for comp_meta in valid_companies:
            comp_id = comp_meta['company_id']
            draft = draft_dict.get(comp_id)
            if not draft:
                print(f"[OutreachGenerator] Missing draft for company {comp_id}. Marking GENERATION_FAILED.")
                try:
                    supabase.table('companies').update({
                        'outreach_status': 'GENERATION_FAILED'
                    }).eq('id', comp_id).execute()
                except Exception as e:
                    print(f"Failed to update status for {comp_id}: {e}")
                continue

            try:
                # Insert draft
                supabase.table('outreach').insert({
                    'company_id': comp_id,
                    'contact_id': comp_meta['contact_id'],
                    'subject': draft.subject,
                    'body': draft.body,
                    'status': 'DRAFT'
                }).execute()
                
                # Update company status
                supabase.table('companies').update({
                    'outreach_status': 'DRAFTED'
                }).eq('id', comp_id).execute()
                
            except Exception as e:
                print(f"[OutreachGenerator] Failed to save draft for company {comp_id}: {e}")
                
        return len(drafts)

    async def start_continuous_loop(self):
        print("[OutreachGenerator] Starting continuous generation loop...")
        while True:
            try:
                processed_count = await self.generate_batch()
                if processed_count > 0:
                    print(f"[OutreachGenerator] Batch of {processed_count} processed. Waiting 10 seconds before next batch...")
                    await asyncio.sleep(10)
                else:
                    # No pending companies or no generation happened, wait longer before checking again
                    await asyncio.sleep(60)
            except Exception as e:
                print(f"[OutreachGenerator] Error in generation loop: {e}")
                await asyncio.sleep(60)
