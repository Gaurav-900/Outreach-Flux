import hashlib
import urllib.parse
from datetime import datetime, timezone
import asyncio

from app.core.supabase import supabase
from app.core.config import get_candidate_profile
from app.providers.base import IDiscoveryProvider
from app.providers.adzuna import AdzunaAdapter
from app.providers.themuse import TheMuseAdapter
from app.providers.aidevjobs import AIDevJobsAdapter
from app.providers.freehire import FreeHireAdapter
from app.providers.signalbase import SignalbaseAdapter
from app.services.matching import MatchingService
from app.services.research import ResearchService
from app.services.contact import ContactService

providers: list[IDiscoveryProvider] = [
    AdzunaAdapter(),
    TheMuseAdapter(),
    AIDevJobsAdapter(),
    FreeHireAdapter(),
    SignalbaseAdapter()
]

class DiscoveryOrchestrator:
    def __init__(self):
        self.candidate_profile = get_candidate_profile()
        self.matching_service = MatchingService(self.candidate_profile)
        self.research_service = ResearchService()
        self.contact_service = ContactService()

    async def run_discovery_for_profile(self, profile_index: int):
        profiles = self.candidate_profile.discovery_profiles
        
        if not profiles:
            print('[DiscoveryOrchestrator] No discovery profiles configured.')
            return
            
        current_profile = profiles[profile_index % len(profiles)]
        if not current_profile:
            print('[DiscoveryOrchestrator] Resolved profile is undefined.')
            return
            
        # The node implementation used `currentProfile.profile_key` for DB state mapping.
        # But the python model DiscoveryProfile doesn't have profile_key. Let's use `current_profile.name` mapped to lower_case no spaces.
        profile_key = current_profile.name.lower().replace(" ", "_")
        
        print(f"[DiscoveryOrchestrator] Running discovery for profile: {current_profile.name}")
        
        for provider in providers:
            if not provider.is_available():
                print(f"[DiscoveryOrchestrator] Skipping provider {provider.name}: Unavailable (missing keys or service down)")
                continue
                
            try:
                print(f"[DiscoveryOrchestrator] Querying provider: {provider.name}")
                
                # Fetch cursor state
                state_data = supabase.table('discovery_provider_state') \
                    .select('*') \
                    .eq('provider', provider.name) \
                    .eq('profile_key', profile_key) \
                    .execute()
                    
                state_record = state_data.data[0] if state_data.data else None
                last_cursor = state_record.get('cursor') if state_record else None
                
                result = await provider.search(current_profile, last_cursor)
                
                print(f"[DiscoveryOrchestrator] {provider.name} returned {len(result.opportunities)} opportunities")
                
                for opp in result.opportunities:
                    await self.process_opportunity(opp.model_dump(), current_profile)
                    
                # Update provider cursor
                supabase.table('discovery_provider_state').upsert({
                    'provider': provider.name,
                    'profile_key': profile_key,
                    'cursor': result.nextCursor,
                    'last_run_at': datetime.now(timezone.utc).isoformat(),
                    'status': 'ACTIVE'
                }, on_conflict='provider,profile_key').execute()
                
            except Exception as e:
                print(f"[DiscoveryOrchestrator] Provider {provider.name} failed: {e}")

    async def process_opportunity(self, opp: dict, discovery_profile):
        company_id = None
        company_data = opp.get('company')
        
        if company_data and company_data.get('name'):
            canonical_domain = None
            if company_data.get('website'):
                parsed_uri = urllib.parse.urlparse(company_data['website'])
                canonical_domain = parsed_uri.hostname.replace('www.', '') if parsed_uri.hostname else None
                
            query = supabase.table('companies').select('id')
            if canonical_domain:
                query = query.eq('canonical_domain', canonical_domain)
            else:
                query = query.eq('name', company_data['name'])
                
            existing_company_res = query.execute()
            existing_company = existing_company_res.data[0] if existing_company_res.data else None
            
            if existing_company:
                company_id = existing_company['id']
            else:
                # Insert company
                new_company_res = supabase.table('companies').insert({
                    'name': company_data['name'],
                    'canonical_domain': canonical_domain,
                    'website': company_data.get('website'),
                    'industry': company_data.get('industry'),
                    'location': company_data.get('location')
                }).execute()
                
                if new_company_res.data:
                    new_company = new_company_res.data[0]
                    company_id = new_company['id']
                    
                    # Insert company source (ignore if conflict)
                    try:
                        supabase.table('company_sources').insert({
                            'company_id': company_id,
                            'provider': opp.get('provider'),
                            'external_id': opp.get('external_id'),
                            'source_url': opp.get('source_url'),
                            'source_metadata': opp.get('source_metadata')
                        }).execute()
                    except Exception:
                        pass
                        
        # 2. Resolve Opportunity Deduplication
        opp_title = opp.get('title', '')
        opp_location = opp.get('location', '')
        hash_data = f"{opp_title}|{company_id}|{opp_location}"
        fallback_external_id = hashlib.sha256(hash_data.encode('utf-8')).hexdigest()
        safe_external_id = opp.get('external_id') or fallback_external_id
        
        existing_source_res = supabase.table('opportunity_sources') \
            .select('opportunity_id') \
            .eq('provider', opp.get('provider')) \
            .eq('external_id', safe_external_id) \
            .execute()
            
        existing_source = existing_source_res.data[0] if existing_source_res.data else None
        
        now_iso = datetime.now(timezone.utc).isoformat()
        
        if existing_source:
            opp_id = existing_source['opportunity_id']
            supabase.table('opportunities').update({'last_seen_at': now_iso}).eq('id', opp_id).execute()
            supabase.table('opportunity_sources').update({'last_seen_at': now_iso}) \
                .eq('provider', opp.get('provider')) \
                .eq('external_id', safe_external_id).execute()
        else:
            match_result = self.matching_service.evaluate_opportunity(opp, discovery_profile)
            status = 'MATCHED' if match_result.isMatch else 'REJECTED'
            
            new_opp_res = supabase.table('opportunities').insert({
                'company_id': company_id,
                'title': opp.get('title'),
                'description': opp.get('description'),
                'location': opp.get('location'),
                'application_url': opp.get('application_url'),
                'status': status,
                'match_score': match_result.score,
                'match_reasons': match_result.reasons
            }).execute()
            
            if new_opp_res.data:
                new_opp = new_opp_res.data[0]
                
                supabase.table('opportunity_sources').insert({
                    'opportunity_id': new_opp['id'],
                    'provider': opp.get('provider'),
                    'external_id': safe_external_id,
                    'source_url': opp.get('source_url'),
                    'source_metadata': opp.get('source_metadata')
                }).execute()
                
                if match_result.isMatch and company_id:
                    target_url = opp.get('application_url')
                    if not target_url and company_data:
                        target_url = company_data.get('website')
                        
                    if target_url:
                        # Fire and forget research task in asyncio
                        asyncio.create_task(self.research_service.research_opportunity(company_id, target_url))
                        # Fire and forget contact discovery task in asyncio
                        asyncio.create_task(self.contact_service.discover_contacts(company_id, target_url))
