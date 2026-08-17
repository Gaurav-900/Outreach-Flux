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
from app.services.matching import MatchingService
from app.services.research import ResearchService
from app.services.contact import ContactService

providers: list[IDiscoveryProvider] = [
    AdzunaAdapter(),
    TheMuseAdapter(),
    AIDevJobsAdapter(),
    FreeHireAdapter()
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
                
                print(f"[DiscoveryOrchestrator] {provider.name} returned {len(result.companies)} companies")
                
                for comp in result.companies:
                    await self.process_company(comp.model_dump(), current_profile)
                    
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

    async def process_company(self, comp_target: dict, discovery_profile):
        company_id = None
        company_data = comp_target.get('company')
        
        if company_data and company_data.get('name'):
            canonical_domain = None
            if company_data.get('website'):
                parsed_uri = urllib.parse.urlparse(company_data['website'])
                canonical_domain = parsed_uri.hostname.replace('www.', '') if parsed_uri.hostname else None
                
            query = supabase.table('companies').select('id, outreach_status')
            if canonical_domain:
                query = query.eq('canonical_domain', canonical_domain)
            else:
                query = query.eq('name', company_data['name'])
                
            existing_company_res = query.execute()
            existing_company = existing_company_res.data[0] if existing_company_res.data else None
            
            if existing_company:
                if existing_company.get('outreach_status') == 'BLACKLISTED':
                    print(f"[DiscoveryOrchestrator] Skipping blacklisted company: {company_data.get('name')}")
                    return
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
                    
            if company_id:
                # Insert company source (ignore if conflict)
                try:
                    supabase.table('company_sources').insert({
                        'company_id': company_id,
                        'provider': comp_target.get('provider'),
                        'external_id': comp_target.get('external_id'),
                        'source_url': comp_target.get('source_url'),
                        'source_metadata': comp_target.get('source_metadata')
                    }).execute()
                except Exception:
                    pass

                target_url = company_data.get('website') or comp_target.get('source_url')
                if target_url:
                    # Fire and forget research task in asyncio
                    asyncio.create_task(self.research_service.research_opportunity(company_id, target_url))
                    # Fire and forget contact discovery task in asyncio
                    asyncio.create_task(self.contact_service.discover_contacts(company_id, target_url))
