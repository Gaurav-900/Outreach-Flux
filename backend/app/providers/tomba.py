import os
import httpx
from typing import List, Optional
from app.providers.contact import ContactProvider
from app.providers.base import NormalizedContact

class TombaAdapter(ContactProvider):
    @property
    def name(self) -> str:
        return "Tomba"

    def is_available(self) -> bool:
        key = os.getenv("TOMBA_KEY")
        secret = os.getenv("TOMBA_SECRET")
        return bool(key and secret)

    async def find_contacts(self, domain: str, company_name: str) -> List[NormalizedContact]:
        if not self.is_available():
            return []

        key = os.getenv("TOMBA_KEY")
        secret = os.getenv("TOMBA_SECRET")

        url = f"https://api.tomba.io/v1/domain-search?domain={domain}"
        headers = {
            "X-Tomba-Key": key,
            "X-Tomba-Secret": secret,
            "User-Agent": "JobOutreachBot/1.0"
        }

        contacts = []
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, timeout=15.0)
                if response.status_code != 200:
                    print(f"[{self.name}] Failed to fetch contacts for {domain}: {response.status_code}")
                    return []
                
                data = response.json()
                emails = data.get("data", {}).get("emails", [])
                for e in emails:
                    email_addr = e.get("email")
                    if not email_addr:
                        continue

                    # Construct name
                    first_name = e.get("first_name")
                    last_name = e.get("last_name")
                    name_parts = [p for p in (first_name, last_name) if p]
                    full_name = " ".join(name_parts) if name_parts else None

                    # Extract source URL if available
                    source_url = None
                    sources = e.get("sources", [])
                    if sources:
                        source_url = sources[0].get("uri")

                    contacts.append(NormalizedContact(
                        name=full_name,
                        role=e.get("position") or e.get("department"),
                        email=email_addr,
                        phone=e.get("phone_number"),
                        source_url=source_url,
                        discovery_method="Tomba"
                    ))

        except Exception as e:
            print(f"[{self.name}] Error searching contacts for {domain}: {e}")

        return contacts
