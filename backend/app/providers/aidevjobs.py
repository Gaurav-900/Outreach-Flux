import os
import httpx
from typing import Optional
from app.providers.base import IDiscoveryProvider, NormalizedOpportunity, ProviderSearchResult, NormalizedCompany
from app.models.candidate import DiscoveryProfile

class AIDevJobsAdapter(IDiscoveryProvider):
    @property
    def name(self) -> str:
        return 'ai_dev_jobs'

    def is_available(self) -> bool:
        return True

    async def search(self, profile: DiscoveryProfile, last_cursor: Optional[str] = None) -> ProviderSearchResult:
        page = int(last_cursor) if last_cursor else 1
        limit = 20
        query = ' '.join(profile.keywords)
        
        url = 'https://aidevboard.com/api/v1/jobs'
        
        params = {
            'page': page,
            'limit': limit,
            'search': query
        }

        headers = {
            'Accept': 'application/json'
        }

        api_key = os.environ.get('AIDEVJOBS_API_KEY')
        if api_key:
            headers['Authorization'] = f'Bearer {api_key}'
            
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, headers=headers)
                response.raise_for_status()
                data = response.json()
                
            results = data.get('data', [])
            
            opportunities = []
            for job in results:
                company_data = job.get('company') or {}
                location_name = job.get('location')
                
                company = NormalizedCompany(
                    name=company_data.get('name', 'Unknown Company'),
                    website=company_data.get('website'),
                    location=location_name
                )
                
                opportunities.append(NormalizedOpportunity(
                    provider=self.name,
                    external_id=str(job.get('id')),
                    source_url=job.get('url'),
                    source_metadata=job,
                    company=company,
                    title=job.get('title'),
                    description=job.get('description'),
                    location=location_name,
                    application_url=job.get('application_url') or job.get('url'),
                    published_at=job.get('published_at') or job.get('created_at')
                ))
                
            meta = data.get('meta') or {}
            has_next_page = bool(meta) and (page * limit) < meta.get('total', 0)
            
            return ProviderSearchResult(
                opportunities=opportunities,
                nextCursor=str(page + 1) if has_next_page else None
            )
            
        except Exception as e:
            print(f"[{self.__class__.__name__}] Search failed: {e}")
            raise e
