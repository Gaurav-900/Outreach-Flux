import json
import os
from pathlib import Path
from typing import Optional
from app.models.candidate import CandidateFile

_CANDIDATE_CACHE: Optional[CandidateFile] = None

def get_candidate_profile() -> CandidateFile:
    global _CANDIDATE_CACHE
    if _CANDIDATE_CACHE is not None:
        return _CANDIDATE_CACHE
        
    config_path = Path(__file__).parent.parent.parent.parent / "config" / "candidate.json"
    
    if not config_path.exists():
        raise FileNotFoundError(f"Candidate profile not found at {config_path}")
        
    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    _CANDIDATE_CACHE = CandidateFile(**data)
    return _CANDIDATE_CACHE
