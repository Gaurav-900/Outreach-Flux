import os
import sys
import json
import hashlib
from pathlib import Path

# Add app to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import get_candidate_profile
from app.services.matching import MatchingService

def run_verification():
    fixture_path = Path(__file__).parent / "fixtures" / "opp_golden_1.json"
    with open(fixture_path, "r") as f:
        opp = json.load(f)

    # 1. Verification: Fingerprint matching (SHA256 of Title|CompanyId|Location)
    # We mock company_id as "mock-company-id-123" for fixture testing
    company_id = "mock-company-id-123"
    opp_title = opp.get('title', '')
    opp_location = opp.get('location', '')
    hash_data = f"{opp_title}|{company_id}|{opp_location}"
    fingerprint = hashlib.sha256(hash_data.encode('utf-8')).hexdigest()
    print(f"Golden Fingerprint: {fingerprint}")
    
    # 2. Verification: Matching logic
    candidate_profile = get_candidate_profile()
    discovery_profile = candidate_profile.discovery_profiles[0] # Pick first
    matching_service = MatchingService(candidate_profile)
    
    result = matching_service.evaluate_opportunity(opp, discovery_profile)
    print(f"Match Result:")
    print(f"  Is Match: {result.isMatch}")
    print(f"  Score: {result.score}")
    print(f"  Reasons: {result.reasons}")
    
    if result.isMatch == False and "Seniority is above candidate target" in result.reasons[0]:
        print("✅ Golden test passed: Senior role was correctly rejected.")
    else:
        print("❌ Golden test failed or needs adjustment based on candidate profile.")

if __name__ == "__main__":
    run_verification()
