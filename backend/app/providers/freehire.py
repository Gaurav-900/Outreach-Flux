import httpx
from typing import Optional
from app.providers.base import IDiscoveryProvider, NormalizedOpportunity, ProviderSearchResult, NormalizedCompany
from app.models.candidate import DiscoveryProfile

class FreeHireAdapter(IDiscoveryProvider):
    @property
    def name(self) -> str:
        return 'freehire'

    def is_available(self) -> bool:
        return True # Public unauthenticated API

    async def search(self, profile: DiscoveryProfile, last_cursor: Optional[str] = None) -> ProviderSearchResult:
        if not self.is_available():
            raise RuntimeError('FreeHire is currently unavailable')

        offset = int(last_cursor) if last_cursor else 0
        limit = 100
        
        # Convert profile query terms to a search string
        query = ' '.join(profile.keywords) # TS: profile.query_terms.join(' ') Wait, TS says query_terms, python model says keywords
        
        url = 'https://freehire.me/api/v1/jobs/search'
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params={
                    'q': query,
                    'limit': limit,
                    'offset': offset
                }, headers={
                    'Accept': 'application/json'
                })
                response.raise_for_status()
                data = response.json()
                
            results = data.get('data', [])
            
            opportunities = []
            for job in results:
                company_data = job.get('company')
                
                if isinstance(company_data, str):
                    company = NormalizedCompany(name=company_data)
                elif isinstance(company_data, dict):
                    company = NormalizedCompany(
                        name=company_data.get('name', 'Unknown Company'),
                        website=company_data.get('website'),
                        location=company_data.get('location')
                    )
                else:
                    company = NormalizedCompany(name='Unknown Company')
                    
                opportunities.append(NormalizedOpportunity(
                    provider=self.name,
                    external_id=str(job.get('id') or job.get('slug')),
                    source_url=job.get('url'),
                    source_metadata=job,
                    company=company,
                    title=job.get('title'),
                    description=job.get('description'),
                    location=job.get('location'),
                    application_url=job.get('application_url') or job.get('url'),
                    published_at=job.get('published_at') or job.get('created_at')
                ))
                
            has_next_page = len(results) == limit
            
            return ProviderSearchResult(
                opportunities=opportunities,
                nextCursor=str(offset + limit) if has_next_page else None
            )
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                print(f"[{self.__class__.__name__}] Rate limit exceeded.")
            else:
                print(f"[{self.__class__.__name__}] Search failed: {e}")
            raise e
        except Exception as e:
            print(f"[{self.__class__.__name__}] Search failed: {e}")
            raise e
