from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.services.scheduler import start_scheduler
from app.services.reply_tracker import ReplyTrackerService

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = start_scheduler()
    yield
    scheduler.shutdown()

app = FastAPI(title="AI Job Outreach API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Same as Express default config
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.core.config import get_candidate_profile

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "Backend is healthy (Python)"}

@app.post("/api/replies/sync")
async def sync_replies():
    try:
        tracker = ReplyTrackerService()
        result = tracker.check_for_replies()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/candidate-profile")
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
