import httpx
from bs4 import BeautifulSoup
import re
from app.core.supabase import supabase

class ResearchService:
    async def research_opportunity(self, company_id: str, url: str | None) -> None:
        if not url:
            print(f"[ResearchService] No URL provided for company {company_id}")
            return
            
        try:
            print(f"[ResearchService] Fetching URL: {url}")
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10.0, headers={
                    'User-Agent': 'Mozilla/5.0 (compatible; JobResearchBot/1.0)'
                })
                response.raise_for_status()
                html = response.text
                
            soup = BeautifulSoup(html, 'html.parser')
            
            # Remove script, style, and noscript tags
            for element in soup(["script", "style", "noscript", "iframe", "img", "svg"]):
                element.decompose()
                
            raw_text = soup.get_text(separator=' ')
            # Collapse whitespace
            raw_text = re.sub(r'\s+', ' ', raw_text).strip()
            
            content = raw_text[:20000]
            
            # Insert into Supabase
            # Using execute() as per supabase-py
            supabase.table('company_research').upsert({
                'company_id': company_id,
                'source_url': url,
                'content': content
            }, on_conflict='company_id,source_url').execute()
            
            print(f"[ResearchService] Successfully researched {url}")
            
        except Exception as e:
            print(f"[ResearchService] Failed to research {url}: {e}")
