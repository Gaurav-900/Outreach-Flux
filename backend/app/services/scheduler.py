import os
import asyncio
from datetime import datetime, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.core.supabase import supabase
from app.core.config import get_candidate_profile
from app.services.automation import AutomationOrchestrator

_is_running = False
orchestrator = AutomationOrchestrator()

async def run_discovery_tick():
    global _is_running
    if _is_running:
        print('[Scheduler] Discovery run already in progress. Skipping overlap.')
        return

    _is_running = True
    try:
        await orchestrator.run_automation_tick()
    except Exception as e:
        print(f'[Scheduler] Error during discovery run: {e}')
    finally:
        _is_running = False

def start_scheduler():
    print('[Scheduler] Starting discovery scheduler (every 1.5 hours)...')
    scheduler = AsyncIOScheduler(timezone='UTC')
    
    # 00:00, 03:00, 06:00, 09:00, 12:00, 15:00, 18:00, 21:00
    scheduler.add_job(run_discovery_tick, CronTrigger(hour='0,3,6,9,12,15,18,21', minute='0'), misfire_grace_time=None, coalesce=True)
    # 01:30, 04:30, 07:30, 10:30, 13:30, 16:30, 19:30, 22:30
    scheduler.add_job(run_discovery_tick, CronTrigger(hour='1,4,7,10,13,16,19,22', minute='30'), misfire_grace_time=None, coalesce=True)
    scheduler.start()
    
    if os.environ.get('RUN_DISCOVERY_ON_STARTUP') == 'true':
        asyncio.create_task(run_discovery_tick())
        
    return scheduler
