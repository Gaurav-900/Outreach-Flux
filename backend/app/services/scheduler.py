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
    print('[Scheduler] Starting discovery scheduler (every 30 minutes)...')
    scheduler = AsyncIOScheduler(timezone='UTC')
    
    # "*/30 * * * *" = Every 30 minutes
    # misfire_grace_time=None ensures it runs even if the event loop was busy and delayed the trigger
    scheduler.add_job(run_discovery_tick, CronTrigger.from_crontab('*/30 * * * *'), misfire_grace_time=None, coalesce=True)
    scheduler.start()
    
    if os.environ.get('RUN_DISCOVERY_ON_STARTUP') == 'true':
        asyncio.create_task(run_discovery_tick())
        
    return scheduler
