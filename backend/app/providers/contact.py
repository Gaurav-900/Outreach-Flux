from abc import ABC, abstractmethod
from typing import List, Optional
from app.providers.base import NormalizedContact

class ContactProvider(ABC):
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
    async def find_contacts(self, domain: str, company_name: str) -> List[NormalizedContact]:
        """Execute a search against the provider to find contacts for a company."""
        pass
