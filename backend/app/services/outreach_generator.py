import os
import asyncio
from typing import List
import json
from datetime import datetime, timezone

from app.core.supabase import supabase
from app.core.config import get_candidate_profile
from app.providers.llm import OpportunityContext, GeminiAdapter, DeepSeekAdapter, EmailDraft

class OutreachGeneratorService:
    def __init__(self):
        self.gemini = GeminiAdapter()
        self.deepseek = DeepSeekAdapter()
        # Fallback batch size to 4 if env var is missing or invalid
        try:
            self.batch_size = int(os.getenv("EMAIL_BATCH_SIZE", "4"))
        except ValueError:
            self.batch_size = 4

    async def generate_batch(self):
        print(f"[OutreachGenerator] Starting generation batch. Max size: {self.batch_size}")
        
        # 1. Fetch READY_FOR_OUTREACH opportunities that don't have drafts yet
        # We fetch opportunities matching 'READY_FOR_OUTREACH'
        res = supabase.table('opportunities').select('*, companies(*), contacts(*)').eq('status', 'READY_FOR_OUTREACH').limit(self.batch_size).execute()
        opportunities = res.data
        
        if not opportunities:
            print("[OutreachGenerator] No opportunities ready for outreach.")
            return

        print(f"[OutreachGenerator] Found {len(opportunities)} opportunities ready for outreach.")
        
        # 2. Prepare Contexts
        candidate_profile = get_candidate_profile()
        # Create a simplified text representation of the profile
        candidate_text = candidate_profile.model_dump_json(exclude_none=True)

        contexts: List[OpportunityContext] = []
        valid_opps = []

        for opp in opportunities:
            # Check if outreach already exists to prevent duplicate generation
            existing = supabase.table('outreach').select('id').eq('opportunity_id', opp['id']).execute()
            if existing.data:
                print(f"[OutreachGenerator] Draft already exists for opportunity {opp['id']}. Skipping.")
                continue

            company = opp.get('companies')
            if not company:
                continue
            
            # Fetch research content
            research_res = supabase.table('company_research').select('content').eq('company_id', company['id']).execute()
            research_content = research_res.data[0]['content'] if research_res.data else None

            # Look for contact
            contacts = opp.get('contacts', [])
            contact = contacts[0] if contacts else None
            
            ctx = OpportunityContext(
                opportunity_id=opp['id'],
                company_name=company.get('name', 'Unknown Company'),
                job_title=opp.get('title', 'Open Role'),
                job_description=opp.get('description'),
                research_content=research_content,
                contact_name=contact.get('name') if contact else None,
                contact_role=contact.get('role') if contact else None,
                candidate_profile=candidate_text
            )
            contexts.append(ctx)
            valid_opps.append({
                'opportunity_id': opp['id'],
                'company_id': company['id'],
                'contact_id': contact['id'] if contact else None
            })

        if not contexts:
            return

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
            print("[OutreachGenerator] All LLM generation attempts failed.")
            return

        print(f"[OutreachGenerator] Successfully generated {len(drafts)} drafts.")

        # 4. Save Drafts & Update Status
        draft_dict = {d.opportunity_id: d for d in drafts}

        for opp_meta in valid_opps:
            opp_id = opp_meta['opportunity_id']
            draft = draft_dict.get(opp_id)
            if not draft:
                print(f"[OutreachGenerator] Missing draft for opportunity {opp_id}.")
                continue

            try:
                # Insert draft
                supabase.table('outreach').insert({
                    'company_id': opp_meta['company_id'],
                    'opportunity_id': opp_id,
                    'contact_id': opp_meta['contact_id'],
                    'subject': draft.subject,
                    'body': draft.body,
                    'status': 'DRAFT'
                }).execute()
                
                # Update opportunity status
                supabase.table('opportunities').update({
                    'status': 'DRAFTED',
                    'updated_at': datetime.now(timezone.utc).isoformat()
                }).eq('id', opp_id).execute()
                
            except Exception as e:
                print(f"[OutreachGenerator] Failed to save draft for opportunity {opp_id}: {e}")
