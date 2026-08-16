import os
import httpx
from typing import Optional
from app.providers.base import IDiscoveryProvider, CompanyTarget, ProviderSearchResult, NormalizedCompany
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
            
            companies = []
            seen_companies = set()
            for job in results:
                company_data = job.get('company') or {}
                company_name = company_data.get('name', 'Unknown Company')
                
                if company_name in seen_companies or company_name == 'Unknown Company':
                    continue
                seen_companies.add(company_name)
                    
                locations = job.get('locations') or []
                location_name = locations[0].get('name') if locations else None
                
                company = NormalizedCompany(
                    name=company_name,
                    location=location_name
                )
                
                refs = job.get('refs') or {}
                
                companies.append(CompanyTarget(
                    provider=self.name,
                    external_id=f"{self.name}_{company_name.lower().replace(' ', '_')}",
                    source_url=refs.get('landing_page'),
                    source_metadata=job,
                    company=company
                ))
                
            has_next_page = page < data.get('page_count', 0)
            
            return ProviderSearchResult(
                companies=companies,
                nextCursor=str(page + 1) if has_next_page else None
            )
            
        except Exception as e:
            print(f"[{self.__class__.__name__}] Search failed: {e}")
            raise e
