import asyncio
import httpx
from bs4 import BeautifulSoup
import re
import urllib.parse
from datetime import datetime, timezone
from typing import List

from app.core.supabase import supabase
from app.providers.tomba import TombaAdapter
from app.providers.base import NormalizedContact

class ContactService:
    def __init__(self, max_concurrent: int = 3):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.tomba_adapter = TombaAdapter()

    async def discover_contacts(self, company_id: str, target_url: str) -> None:
        async with self.semaphore:
            # 1. Idempotency Check: Have we already processed this company?
            state_res = supabase.table('contact_discovery_state').select('status').eq('company_id', company_id).execute()
            if state_res.data and state_res.data[0]['status'] in ('COMPLETED', 'FAILED'):
                print(f"[ContactService] Contact discovery already {state_res.data[0]['status']} for company {company_id}. Skipping.")
                return

            print(f"[ContactService] Starting contact discovery for {company_id} at {target_url}")
            try:
                supabase.table('contact_discovery_state').upsert({
                    'company_id': company_id,
                    'status': 'IN_PROGRESS',
                    'last_run_at': datetime.now(timezone.utc).isoformat()
                }).execute()
            except Exception as e:
                print(f"[ContactService] Error setting IN_PROGRESS state: {e}")

            contacts_found: List[NormalizedContact] = []
            
            # 2. Public Page Extraction
            try:
                public_contacts = await self._extract_public_contacts(target_url)
                contacts_found.extend(public_contacts)
            except Exception as e:
                print(f"[ContactService] Public extraction failed for {target_url}: {e}")

            # 3. Tomba Fallback
            if not contacts_found:
                print(f"[ContactService] No public contacts found for {company_id}. Attempting Tomba fallback.")
                try:
                    domain = self._extract_domain(target_url)
                    if domain:
                        tomba_contacts = await self.tomba_adapter.find_contacts(domain, company_name="")
                        contacts_found.extend(tomba_contacts)
                except Exception as e:
                    print(f"[ContactService] Tomba fallback failed for {company_id}: {e}")

            # 4. Filter and Prioritize (Careers > HR > General) - simplistic sort
            # For this MVP, we just take what we have.
            
            # 5. Persist Contacts
            for contact in contacts_found:
                try:
                    supabase.table('contacts').upsert({
                        'company_id': company_id,
                        'name': contact.name,
                        'role': contact.role,
                        'email': contact.email.lower().strip(),
                        'phone': contact.phone,
                        'source_url': contact.source_url,
                        'discovery_method': contact.discovery_method
                    }, on_conflict='company_id,email').execute()
                except Exception as e:
                    print(f"[ContactService] Failed to insert contact {contact.email}: {e}")
            
            # Update state to completed
            try:
                supabase.table('contact_discovery_state').upsert({
                    'company_id': company_id,
                    'status': 'COMPLETED',
                    'last_run_at': datetime.now(timezone.utc).isoformat()
                }).execute()
                print(f"[ContactService] Contact discovery completed for {company_id}. Found {len(contacts_found)} contacts.")
                
                # If we found contacts, update MATCHED opportunities to READY_FOR_OUTREACH
                if contacts_found:
                    supabase.table('opportunities').update({
                        'status': 'READY_FOR_OUTREACH',
                        'updated_at': datetime.now(timezone.utc).isoformat()
                    }).eq('company_id', company_id).eq('status', 'MATCHED').execute()
                    print(f"[ContactService] Updated MATCHED opportunities to READY_FOR_OUTREACH for company {company_id}.")
            except Exception as e:
                print(f"[ContactService] Error setting COMPLETED state: {e}")

    async def _extract_public_contacts(self, target_url: str) -> List[NormalizedContact]:
        if not target_url:
            return []

        contacts = []
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(target_url, timeout=10.0, headers={
                    'User-Agent': 'Mozilla/5.0 (compatible; JobOutreachBot/1.0)'
                })
                response.raise_for_status()
                html = response.text
                
            soup = BeautifulSoup(html, 'html.parser')
            
            # Search for mailto links
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                if href.lower().startswith("mailto:"):
                    email = href[7:].split('?')[0].strip()
                    if self._is_valid_email(email):
                        contacts.append(NormalizedContact(
                            email=email,
                            source_url=target_url,
                            discovery_method="Public Page Extraction (mailto)"
                        ))

            # Regex search for emails in text (avoiding overly broad matches, simple heuristic)
            text_content = soup.get_text(separator=' ')
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            for match in re.finditer(email_pattern, text_content):
                email = match.group().strip()
                # filter out obvious false positives (png, jpg, etc.)
                if email.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.css', '.js', '.webp')):
                    continue
                if self._is_valid_email(email) and not any(c.email == email for c in contacts):
                    contacts.append(NormalizedContact(
                        email=email,
                        source_url=target_url,
                        discovery_method="Public Page Extraction (Regex)"
                    ))
                    
        except Exception:
            pass # Silently fail and fallback

        return contacts

    def _is_valid_email(self, email: str) -> bool:
        if not email or "@" not in email:
            return False
        # simple check
        parts = email.split("@")
        if len(parts) != 2 or not parts[0] or not parts[1]:
            return False
        return True

    def _extract_domain(self, url: str) -> str | None:
        if not url:
            return None
        if not url.startswith("http"):
            url = "http://" + url
        try:
            parsed = urllib.parse.urlparse(url)
            hostname = parsed.hostname
            if hostname:
                return hostname.replace('www.', '')
        except Exception:
            pass
        return None
