import re
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from app.models.candidate import CandidateFile, DiscoveryProfile

class MatchResult(BaseModel):
    isMatch: bool
    score: int
    reasons: List[str]

class MatchingService:
    def __init__(self, candidate_profile: CandidateFile):
        self.candidate_profile = candidate_profile

    def evaluate_opportunity(self, opportunity: Dict[str, Any], discovery_profile: Optional[DiscoveryProfile] = None) -> MatchResult:
        reasons = []
        
        # We assume candidate_profile data exists as dict via model_dump() if needed, but we can access attributes
        # Since we use CandidateFile pydantic model, it might not have 'matching_rules'. 
        # Wait, the node candidate.json has matching_rules, skills, discovery_preferences.
        # Let's read them dynamically or assume they are dicts if they weren't strictly typed.
        # Let me use dict access if it's dynamic, but I defined CandidateFile without matching_rules. 
        # I should just access them via raw dict or use getattr since the candidate.json structure is robust.
        
        # Let's fetch raw data from candidate profile dict
        profile_data = self.candidate_profile.model_dump(exclude_unset=True)
        # Note: the typescript models had matching_rules, skills, discovery_preferences
        
        matching_rules = profile_data.get('matching_rules') or {}
        hard_filters = matching_rules.get('hard_filters') or {}
        discovery_prefs = profile_data.get('discovery_preferences') or {}
        skills = profile_data.get('skills') or {}
        
        title = opportunity.get('title', '')
        title_lower = title.lower()
        
        # 1. Role Filter
        if hard_filters.get('reject_if_role_is_clearly_unrelated'):
            all_keywords = []
            all_keywords.extend(discovery_prefs.get('target_roles') or [])
            if discovery_profile and discovery_profile.keywords:
                all_keywords.extend(discovery_profile.keywords)
                
            all_keywords_lower = [k.lower() for k in all_keywords]
            
            is_role_related = any(kw in title_lower for kw in all_keywords_lower) or \
                              'developer' in title_lower or \
                              'engineer' in title_lower or \
                              'intern' in title_lower or \
                              'programmer' in title_lower
                              
            if not is_role_related:
                return MatchResult(isMatch=False, score=0, reasons=['Role is clearly unrelated based on title.'])

        # 2. Seniority Filter
        if hard_filters.get('reject_if_seniority_above_candidate'):
            senior_keywords = ['senior', 'principal', 'staff', 'lead', 'manager', 'director', 'head', 'vp']
            has_senior_keyword = any(kw in title_lower for kw in senior_keywords)
            
            words = re.split(r'[\s,\.-]+', title_lower)
            has_sr = 'sr' in words or 'senior' in words
            
            if has_senior_keyword or has_sr:
                return MatchResult(isMatch=False, score=0, reasons=['Seniority is above candidate target (Intern/Junior/Entry).'])

        # 3. Location Filter
        location = opportunity.get('location')
        if hard_filters.get('reject_if_location_explicitly_incompatible') and location:
            loc_lower = location.lower()
            pref_locs = [l.lower() for l in (discovery_prefs.get('preferred_locations') or [])]
            work_modes = [m.lower() for m in (discovery_prefs.get('preferred_work_modes') or [])]
            
            # Basic heuristic
            if 'us only' in loc_lower or 'united states only' in loc_lower:
                if not any('us' in l or 'united states' in l for l in pref_locs):
                    return MatchResult(isMatch=False, score=0, reasons=['Location is explicitly incompatible (e.g. US Only).'])

        # 4. Scoring
        score = 50
        reasons.append('Passed hard filters. Base score 50.')
        
        preferred_signals = matching_rules.get('preferred_match_signals') or []
        
        desc_lower = (opportunity.get('description') or '').lower()
        
        for signal in preferred_signals:
            kw = signal.lower()
            if kw in desc_lower or kw in title_lower:
                score += 5
                reasons.append(f'Matched preferred signal: {signal}')
                
        candidate_skills = []
        candidate_skills.extend(skills.get('frontend') or [])
        candidate_skills.extend(skills.get('backend_and_data') or [])
        candidate_skills.extend(skills.get('automation_and_infrastructure') or [])
        
        preferred_signals_lower = [s.lower() for s in preferred_signals]
        
        for skill in candidate_skills:
            kw = re.sub(r' \(.+\)', '', skill).lower()
            if kw in desc_lower or kw in title_lower:
                if kw not in preferred_signals_lower:
                    score += 2
                    reasons.append(f'Matched candidate skill: {skill}')
                    
        score = min(score, 100)
        
        return MatchResult(isMatch=True, score=score, reasons=reasons)
