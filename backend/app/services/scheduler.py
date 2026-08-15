import os
import asyncio
from datetime import datetime, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.core.supabase import supabase
from app.core.config import get_candidate_profile
from app.services.orchestrator import DiscoveryOrchestrator

_is_running = False
orchestrator = DiscoveryOrchestrator()

async def run_discovery_tick():
    global _is_running
    if _is_running:
        print('[Scheduler] Discovery run already in progress. Skipping overlap.')
        return

    _is_running = True
    try:
        print('[Scheduler] Starting discovery rotation tick...')
        
        candidate_config = get_candidate_profile()
        profiles_count = len(candidate_config.discovery_profiles)
        
        if profiles_count == 0:
            print('[Scheduler] No discovery profiles found in candidate.json.')
            return

        state_res = supabase.table('discovery_state') \
            .select('*') \
            .order('updated_at', desc=True) \
            .limit(1) \
            .execute()
            
        state_data = state_res.data[0] if state_res.data else None
        
        next_index = 0
        state_id = None

        if state_data:
            state_id = state_data['id']
            last_index = state_data.get('last_profile_index', 0)
            next_index = (last_index + 1) % profiles_count

        await orchestrator.run_discovery_for_profile(next_index)

        now_iso = datetime.now(timezone.utc).isoformat()
        
        if state_id:
            supabase.table('discovery_state').update({
                'last_run_at': now_iso,
                'last_profile_index': next_index,
                'updated_at': now_iso
            }).eq('id', state_id).execute()
        else:
            supabase.table('discovery_state').insert({
                'last_run_at': now_iso,
                'last_profile_index': next_index
            }).execute()

        print('[Scheduler] Discovery rotation tick completed.')
        
    except Exception as e:
        print(f'[Scheduler] Error during discovery run: {e}')
    finally:
        _is_running = False

def start_scheduler():
    print('[Scheduler] Starting discovery scheduler (every 3 hours)...')
    scheduler = AsyncIOScheduler(timezone='UTC')
    
    # "0 */3 * * *" = At minute 0 past every 3rd hour
    scheduler.add_job(run_discovery_tick, CronTrigger.from_crontab('0 */3 * * *'))
    scheduler.start()
    
    if os.environ.get('RUN_DISCOVERY_ON_STARTUP') == 'true':
        asyncio.create_task(run_discovery_tick())
        
    return scheduler
