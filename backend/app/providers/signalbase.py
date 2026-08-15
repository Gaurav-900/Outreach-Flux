import os
import httpx
from typing import Optional
from app.providers.base import IDiscoveryProvider, NormalizedOpportunity, ProviderSearchResult, NormalizedCompany
from app.models.candidate import DiscoveryProfile

class SignalbaseAdapter(IDiscoveryProvider):
    @property
    def name(self) -> str:
        return 'signalbase'

    def is_available(self) -> bool:
        return bool(os.environ.get('SIGNALBASE_API_KEY'))

    async def search(self, profile: DiscoveryProfile, last_cursor: Optional[str] = None) -> ProviderSearchResult:
        if not self.is_available():
            raise RuntimeError('Signalbase credentials are not configured')

        page = int(last_cursor) if last_cursor else 1
        limit = 100
        
        url = 'https://www.trysignalbase.com/api/v2/signals/funding'
        
        params = {
            'page': page,
            'limit': limit,
            'date_preset': 'last_30_days'
        }

        headers = {
            'Accept': 'application/json',
            'Authorization': f"Bearer {os.environ.get('SIGNALBASE_API_KEY')}"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, headers=headers)
                response.raise_for_status()
                data = response.json()
                
            results = data.get('data', [])
            
            opportunities = []
            for signal in results:
                company = NormalizedCompany(
                    name=signal.get('companyName', 'Unknown Company'),
                    website=signal.get('companyWebsite'),
                    industry=signal.get('companySubcategory'),
                    location=signal.get('companyCountry')
                )
                
                investors = ', '.join(signal.get('investorNames') or [])
                description = f"Raised {signal.get('fundingAmount')}. Investors: {investors}. Match confidence: {signal.get('match_confidence')}"
                
                source_metadata = dict(signal)
                source_metadata['provenance_timestamp'] = signal.get('discoveredAt') or signal.get('occurredAt')
                
                opportunities.append(NormalizedOpportunity(
                    provider=self.name,
                    external_id=str(signal.get('signalId')),
                    source_url=signal.get('companyWebsite'),
                    source_metadata=source_metadata,
                    company=company,
                    title=f"Funding Round: {signal.get('companyName')} ({signal.get('roundType')})",
                    description=description,
                    location=signal.get('companyCountry'),
                    application_url=signal.get('companyWebsite'),
                    published_at=signal.get('announcedDate') or signal.get('occurredAt')
                ))
                
            pagination = data.get('pagination') or {}
            has_next_page = pagination.get('hasNextPage', False)
            
            return ProviderSearchResult(
                opportunities=opportunities,
                nextCursor=str(page + 1) if has_next_page else None
            )
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                print(f"[{self.__class__.__name__}] Unauthorized: Invalid or missing API Key.")
            elif e.response.status_code == 429:
                print(f"[{self.__class__.__name__}] Rate limit exceeded.")
            else:
                print(f"[{self.__class__.__name__}] Search failed: {e}")
            raise e
        except Exception as e:
            print(f"[{self.__class__.__name__}] Search failed: {e}")
            raise e
