import os
import sys
import asyncio
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.supabase import supabase
from app.core.config import get_candidate_profile
from app.providers.freehire import FreeHireAdapter
from app.providers.themuse import TheMuseAdapter
from app.services.orchestrator import DiscoveryOrchestrator
from app.services.scheduler import run_discovery_tick

async def run_tests():
    print("=== REGRESSION TEST MATRIX ===")
    
    # R3: Config Load
    print("\n--- R3: Config Load ---")
    try:
        profile = get_candidate_profile()
        print(f"✅ Config loaded. Name: {profile.candidate.name}, Profiles count: {len(profile.discovery_profiles)}")
    except Exception as e:
        print(f"❌ R3 Failed: {e}")

    # R5: FreeHire Provider
    print("\n--- R5: Provider (FreeHire) ---")
    try:
        adapter = FreeHireAdapter()
        # Mock a narrow search to return few results quickly
        test_profile = profile.discovery_profiles[0].model_copy()
        test_profile.query_terms = ["React Developer"]
        res = await adapter.search(test_profile)
        print(f"✅ FreeHire Provider parsed API. Returned {len(res.opportunities)} opportunities.")
    except Exception as e:
        print(f"❌ R5 Failed: {e}")

    # R6: The Muse Provider
    print("\n--- R6: Provider (The Muse) ---")
    try:
        adapter = TheMuseAdapter()
        res = await adapter.search(profile.discovery_profiles[0])
        print(f"✅ The Muse Provider parsed API. Returned {len(res.opportunities)} opportunities.")
    except Exception as e:
        print(f"❌ R6 Failed: {e}")

    # R10: Scheduler & R7/R9 implied
    print("\n--- R10: Scheduler Trigger Tick ---")
    try:
        # Get current state before
        state_before = supabase.table('discovery_state').select('*').order('updated_at', desc=True).limit(1).execute()
        idx_before = state_before.data[0].get('last_profile_index') if state_before.data else None
        print(f"State index before tick: {idx_before}")
        
        # Run tick (this will trigger R7 Orchestrator and R9 background research)
        await run_discovery_tick()
        
        # Get current state after
        state_after = supabase.table('discovery_state').select('*').order('updated_at', desc=True).limit(1).execute()
        idx_after = state_after.data[0].get('last_profile_index') if state_after.data else None
        print(f"✅ Scheduler Tick completed. State index after tick: {idx_after}")
        
    except Exception as e:
        print(f"❌ R10 Failed: {e}")

if __name__ == "__main__":
    asyncio.run(run_tests())
