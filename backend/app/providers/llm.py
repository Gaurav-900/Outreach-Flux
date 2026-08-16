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
    company_id: str
    subject: str
    body: str

class EmailBatchResponse(BaseModel):
    drafts: List[EmailDraft]

class CompanyContext(BaseModel):
    company_id: str
    company_name: str
    research_content: Optional[str] = None
    contact_name: Optional[str] = None
    contact_role: Optional[str] = None
    candidate_profile: str
    location_preference: Optional[str] = None

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
    async def generate_drafts(self, contexts: List[CompanyContext]) -> List[EmailDraft]:
        """Generate personalized email drafts for a batch of companies."""
        pass

def _build_prompt(contexts: List[CompanyContext]) -> str:
    prompt = "You write short, natural speculative outreach emails for an engineer looking for a role at the provided company.\n"
    prompt += "Write like a real person reaching out directly to a hiring manager or founder, not an AI.\n\n"
    prompt += "Rules:\n"
    prompt += "- Keep the email medium-short and easy to read.\n"
    prompt += "- Clearly mention the candidate's most relevant skills/experience.\n"
    prompt += "- Explicitly state the candidate's location preference (e.g., remote, specific city) if provided.\n"
    prompt += "- Explain naturally why the candidate would be a great fit for the company's domain or tech stack.\n"
    prompt += "- Use simple, conversational professional language.\n"
    prompt += "- Avoid generic phrases like 'I am writing to express my interest' or 'I hope this email finds you well.'\n"
    prompt += "- Do not exaggerate, invent skills, experience, achievements, or company information.\n"
    prompt += "- Do not repeat the resume unnecessarily.\n"
    prompt += "- Use proper paragraphs and line breaks (ensure they are properly escaped in the JSON output as \\n\\n for multiple paragraphs).\n"
    prompt += "- Do not use bullet points unless specifically useful.\n"
    prompt += "- Keep the email concise enough that a busy person will actually read it.\n"
    prompt += "- End with a simple, natural call to action (e.g. asking for a brief chat if they are hiring).\n"
    prompt += "- Return only the email body. No subject line, explanation, or commentary.\n\n"
    prompt += "Below is a list of companies with their context. Write a personalized email draft for each.\n"
    prompt += "Ensure the output is a JSON array matching the requested schema.\n\n"
    for ctx in contexts:
        prompt += f"Company ID: {ctx.company_id}\n"
        prompt += f"Company: {ctx.company_name}\n"
        if ctx.research_content:
            prompt += f"Company Research: {ctx.research_content[:1500]}...\n"
        if ctx.contact_name:
            prompt += f"Contact Name: {ctx.contact_name} ({ctx.contact_role or 'Unknown role'})\n"
        if ctx.location_preference:
            prompt += f"Location Preference: {ctx.location_preference}\n"
        prompt += f"Candidate Profile Context: {ctx.candidate_profile[:2000]}...\n"
        prompt += "-" * 40 + "\n"
    return prompt

class GeminiAdapter(LLMProvider):
    @property
    def name(self) -> str:
        return "Gemini"

    def is_available(self) -> bool:
        return bool(os.getenv("GEMINI_API_KEY")) and genai is not None

    async def generate_drafts(self, contexts: List[CompanyContext]) -> List[EmailDraft]:
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

    async def generate_drafts(self, contexts: List[CompanyContext]) -> List[EmailDraft]:
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
