import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.services.scheduler import start_scheduler
from app.services.reply_tracker import ReplyTrackerService
from app.api.dependencies import get_current_user

import asyncio
from app.services.outreach_generator import OutreachGeneratorService

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = start_scheduler()
    generator = OutreachGeneratorService()
    generator_task = asyncio.create_task(generator.start_continuous_loop())
    yield
    scheduler.shutdown()
    generator_task.cancel()

app = FastAPI(title="AI Job Outreach API", lifespan=lifespan)

frontend_url = os.environ.get("FRONTEND_URL", "http://localhost:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.core.config import get_candidate_profile

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "Backend is healthy (Python)"}

@app.post("/api/replies/sync", dependencies=[Depends(get_current_user)])
async def sync_replies():
    try:
        tracker = ReplyTrackerService()
        result = tracker.check_for_replies()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from app.services.sending_policy import SendingOrchestrator

@app.post("/api/outreach/trigger-sending", dependencies=[Depends(get_current_user)])
async def trigger_sending():
    try:
        sender = SendingOrchestrator()
        sender.process_queue()
        return {"status": "success", "message": "Queue processed."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/candidate-profile", dependencies=[Depends(get_current_user)])
async def get_candidate_profile_endpoint():
    profile = get_candidate_profile()
    
    # Sanitized output
    return {
        "name": profile.candidate.name,
        "location": profile.candidate.location.model_dump() if profile.candidate.location else None,
        "professional_profile": profile.professional_profile.model_dump() if profile.professional_profile else None,
        "discovery_preferences": profile.discovery_preferences.model_dump(),
        "discovery_profiles": [p.model_dump() for p in profile.discovery_profiles]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
