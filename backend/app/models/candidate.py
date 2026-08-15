from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class CandidateContact(BaseModel, extra="allow"):
    email: str
    phone: Optional[str] = None

class CandidateLocation(BaseModel, extra="allow"):
    city: Optional[str] = None
    country: Optional[str] = None

class CandidateEducation(BaseModel, extra="allow"):
    institution: str
    program: Optional[str] = None
    qualification: Optional[str] = None
    expected_completion_year: Optional[int] = None
    completion: Optional[str] = None
    status: Optional[str] = None

class CandidateInfo(BaseModel, extra="allow"):
    name: str
    contact: CandidateContact
    location: Optional[CandidateLocation] = None
    profiles: Optional[Dict[str, str]] = None
    education: Optional[List[CandidateEducation]] = None

class ProfessionalProfile(BaseModel, extra="allow"):
    summary: Optional[str] = None
    primary_direction: Optional[str] = None
    secondary_directions: Optional[List[str]] = None
    career_stage: Optional[str] = None
    strengths: Optional[List[str]] = None

class Experience(BaseModel, extra="allow"):
    organization: str
    role: str
    start: Optional[str] = None
    end: Optional[str] = None
    status: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    technology: Optional[List[str]] = None
    details: Optional[List[str]] = None

class Project(BaseModel, extra="allow"):
    name: str
    url: Optional[str] = None
    label: Optional[str] = None
    stack: Optional[List[str]] = None
    details: Optional[List[str]] = None

class Skills(BaseModel, extra="allow"):
    languages: Optional[List[str]] = None
    frontend: Optional[List[str]] = None
    backend_and_data: Optional[List[str]] = None
    automation_and_infrastructure: Optional[List[str]] = None

class DiscoveryPreferences(BaseModel, extra="allow"):
    target_roles: List[str]
    preferred_locations: List[str]
    target_seniority: List[str]
    target_employment_types: List[str]
    preferred_work_modes: List[str]
    target_industries: List[str]
    priority_skills: List[str]

class DiscoveryProfile(BaseModel, extra="allow"):
    profile_key: str
    label: str
    query_terms: List[str]
    skill_focus: List[str]

    @property
    def keywords(self) -> List[str]:
        return self.query_terms
        
    @property
    def name(self) -> str:
        return self.label

class MatchingRules(BaseModel, extra="allow"):
    hard_filters: Optional[Dict[str, bool]] = None
    preferred_match_signals: Optional[List[str]] = None
    related_role_policy: Optional[str] = None

class OutreachPreferences(BaseModel, extra="allow"):
    resume_attachment_required: Optional[bool] = None
    resume_path: Optional[str] = None
    resume_attachment_filename: Optional[str] = None
    email_batch_size: Optional[int] = None
    personalization_rules: Optional[List[str]] = None

class CandidateFile(BaseModel, extra="allow"):
    schema_version: Optional[str] = None
    candidate: CandidateInfo
    professional_profile: Optional[ProfessionalProfile] = None
    experience: Optional[List[Experience]] = None
    projects: Optional[List[Project]] = None
    skills: Optional[Skills] = None
    discovery_preferences: DiscoveryPreferences
    discovery_profiles: List[DiscoveryProfile]
    matching_rules: Optional[MatchingRules] = None
    outreach_preferences: Optional[OutreachPreferences] = None
    source_provenance: Optional[Dict[str, str]] = None
