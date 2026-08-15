from typing import Optional, List, Any
from pydantic import BaseModel
from abc import ABC, abstractmethod
from app.models.candidate import DiscoveryProfile

class NormalizedCompany(BaseModel):
    name: str
    website: Optional[str] = None
    industry: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    careers_url: Optional[str] = None

class NormalizedOpportunity(BaseModel):
    provider: str
    external_id: str
    source_url: Optional[str] = None
    source_metadata: Any
    company: NormalizedCompany
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    application_url: Optional[str] = None
    published_at: Optional[str] = None

class ProviderSearchResult(BaseModel):
    opportunities: List[NormalizedOpportunity]
    nextCursor: Optional[str] = None

class IDiscoveryProvider(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """The unique identifier for this provider."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Determines if the provider is currently available (e.g., API keys are present)."""
        pass

    @abstractmethod
    async def search(self, profile: DiscoveryProfile, last_cursor: Optional[str] = None) -> ProviderSearchResult:
        """Execute a search against the provider."""
        pass
