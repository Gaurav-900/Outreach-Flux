import os
import httpx
from typing import Optional
from app.providers.base import IDiscoveryProvider, NormalizedOpportunity, ProviderSearchResult, NormalizedCompany
from app.models.candidate import DiscoveryProfile

class TheMuseAdapter(IDiscoveryProvider):
    @property
    def name(self) -> str:
        return 'the_muse'

    def is_available(self) -> bool:
        return True # The Muse allows public unauthenticated access

    async def search(self, profile: DiscoveryProfile, last_cursor: Optional[str] = None) -> ProviderSearchResult:
        page = int(last_cursor) if last_cursor else 1
        
        url = 'https://www.themuse.com/api/public/jobs'
        
        params = {
            'page': page,
            'category': ['Computer and IT', 'Software Engineer', 'Data and Analytics']
        }

        api_key = os.environ.get('THEMUSE_API_KEY')
        if api_key:
            params['api_key'] = api_key
            
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
            results = data.get('results', [])
            
            opportunities = []
            for job in results:
                company_data = job.get('company') or {}
                locations = job.get('locations') or []
                location_name = locations[0].get('name') if locations else None
                
                company = NormalizedCompany(
                    name=company_data.get('name', 'Unknown Company'),
                    location=location_name
                )
                
                refs = job.get('refs') or {}
                
                opportunities.append(NormalizedOpportunity(
                    provider=self.name,
                    external_id=str(job.get('id')),
                    source_url=refs.get('landing_page'),
                    source_metadata=job,
                    company=company,
                    title=job.get('name'),
                    description=job.get('contents'),
                    location=location_name,
                    application_url=refs.get('landing_page'),
                    published_at=job.get('publication_date')
                ))
                
            has_next_page = page < data.get('page_count', 0)
            
            return ProviderSearchResult(
                opportunities=opportunities,
                nextCursor=str(page + 1) if has_next_page else None
            )
            
        except Exception as e:
            print(f"[{self.__class__.__name__}] Search failed: {e}")
            raise e
