import os
import httpx
from typing import Optional
from app.providers.base import IDiscoveryProvider, CompanyTarget, ProviderSearchResult, NormalizedCompany
from app.models.candidate import DiscoveryProfile

class AdzunaAdapter(IDiscoveryProvider):
    @property
    def name(self) -> str:
        return 'adzuna'

    def is_available(self) -> bool:
        return bool(os.environ.get('ADZUNA_APP_ID') and os.environ.get('ADZUNA_APP_KEY'))

    async def search(self, profile: DiscoveryProfile, last_cursor: Optional[str] = None) -> ProviderSearchResult:
        if not self.is_available():
            raise RuntimeError('Adzuna credentials are not configured')

        app_id = os.environ.get('ADZUNA_APP_ID')
        app_key = os.environ.get('ADZUNA_APP_KEY')
        
        page = int(last_cursor) if last_cursor else 1
        limit = 50
        country = 'us'

        query = ' '.join(profile.keywords)
        
        url = f'https://api.adzuna.com/v1/api/jobs/{country}/search/{page}'
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params={
                    'app_id': app_id,
                    'app_key': app_key,
                    'results_per_page': limit,
                    'what': query,
                    'content-type': 'application/json'
                })
                response.raise_for_status()
                data = response.json()
                
            results = data.get('results', [])
            
            companies = []
            seen_companies = set()
            for job in results:
                company_data = job.get('company') or {}
                company_name = company_data.get('display_name', 'Unknown Company')
                
                if company_name in seen_companies or company_name == 'Unknown Company':
                    continue
                seen_companies.add(company_name)
                    
                location_data = job.get('location') or {}
                location_name = location_data.get('display_name')
                
                company = NormalizedCompany(
                    name=company_name,
                    location=location_name
                )
                
                companies.append(CompanyTarget(
                    provider=self.name,
                    external_id=f"{self.name}_{company_name.lower().replace(' ', '_')}",
                    source_url=job.get('redirect_url'),
                    source_metadata=job,
                    company=company
                ))
                
            has_next_page = (page * limit) < data.get('count', 0)
            
            return ProviderSearchResult(
                companies=companies,
                nextCursor=str(page + 1) if has_next_page else None
            )
            
        except Exception as e:
            print(f"[{self.__class__.__name__}] Search failed: {e}")
            raise e
