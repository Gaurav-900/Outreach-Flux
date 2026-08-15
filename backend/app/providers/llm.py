from abc import ABC, abstractmethod
from typing import List, Optional
from pydantic import BaseModel
import os
import json
import httpx
try:
    from google import genai
except ImportError:
    genai = None

class EmailDraft(BaseModel):
    opportunity_id: str
    subject: str
    body: str

class EmailBatchResponse(BaseModel):
    drafts: List[EmailDraft]

class OpportunityContext(BaseModel):
    opportunity_id: str
    company_name: str
    job_title: str
    job_description: Optional[str] = None
    research_content: Optional[str] = None
    contact_name: Optional[str] = None
    contact_role: Optional[str] = None
    candidate_profile: str

class LLMProvider(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """The unique identifier for this provider."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Determines if the provider is currently available."""
        pass

    @abstractmethod
    async def generate_drafts(self, contexts: List[OpportunityContext]) -> List[EmailDraft]:
        """Generate personalized email drafts for a batch of opportunities."""
        pass

def _build_prompt(contexts: List[OpportunityContext]) -> str:
    prompt = "You are an expert AI outreach assistant writing highly personalized job application and networking emails.\n\n"
    prompt += "Below is a list of opportunities with their context. Write a personalized email draft for each.\n"
    prompt += "Do not invent any facts, experiences, or skills that are not present in the candidate profile.\n"
    prompt += "Ensure the output is a JSON array matching the requested schema.\n\n"
    for ctx in contexts:
        prompt += f"Opportunity ID: {ctx.opportunity_id}\n"
        prompt += f"Company: {ctx.company_name}\n"
        prompt += f"Job Title: {ctx.job_title}\n"
        if ctx.job_description:
            prompt += f"Job Description Summary: {ctx.job_description[:1000]}...\n"
        if ctx.research_content:
            prompt += f"Company Research: {ctx.research_content[:1500]}...\n"
        if ctx.contact_name:
            prompt += f"Contact Name: {ctx.contact_name} ({ctx.contact_role or 'Unknown role'})\n"
        prompt += f"Candidate Profile Context: {ctx.candidate_profile[:2000]}...\n"
        prompt += "-" * 40 + "\n"
    return prompt

class GeminiAdapter(LLMProvider):
    @property
    def name(self) -> str:
        return "Gemini"

    def is_available(self) -> bool:
        return bool(os.getenv("GEMINI_API_KEY")) and genai is not None

    async def generate_drafts(self, contexts: List[OpportunityContext]) -> List[EmailDraft]:
        if not self.is_available() or not contexts:
            return []
            
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        prompt = _build_prompt(contexts)
        
        # We need to run the synchronous SDK call in a thread pool since google-genai is sync by default unless using async client
        # Let's use the async client if available or just run in executor
        # google-genai has client.aio
        try:
            response = await client.aio.models.generate_content(
                model='gemini-3.7-flash',
                contents=prompt,
                config={
                    'response_mime_type': 'application/json',
                    'response_schema': EmailBatchResponse,
                    'temperature': 0.7,
                }
            )
            # Response is typically a JSON string matching the schema
            result_json = response.text
            parsed = EmailBatchResponse.model_validate_json(result_json)
            return parsed.drafts
        except Exception as e:
            print(f"[{self.name}] Failed to generate drafts: {e}")
            return []

class DeepSeekAdapter(LLMProvider):
    @property
    def name(self) -> str:
        return "DeepSeek"

    def is_available(self) -> bool:
        return bool(os.getenv("DEEPSEEK_API_KEY"))

    async def generate_drafts(self, contexts: List[OpportunityContext]) -> List[EmailDraft]:
        if not self.is_available() or not contexts:
            return []
            
        prompt = _build_prompt(contexts)
        prompt += "\nOutput exactly a JSON object with a 'drafts' key containing the array of email drafts. Each draft must have 'opportunity_id', 'subject', and 'body'."
        
        headers = {
            "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-v4-flash",
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant that outputs JSON."},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.7
        }
        
        try:
            async with httpx.AsyncClient() as client:
                res = await client.post("https://api.deepseek.com/chat/completions", headers=headers, json=payload, timeout=60.0)
                res.raise_for_status()
                data = res.json()
                content = data['choices'][0]['message']['content']
                parsed = EmailBatchResponse.model_validate_json(content)
                return parsed.drafts
        except Exception as e:
            print(f"[{self.name}] Failed to generate drafts: {e}")
            return []
