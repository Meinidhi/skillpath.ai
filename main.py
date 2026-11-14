import os
import sys

# Ensure backend and project root are on sys.path
backend_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(backend_dir)
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import SessionLocal, engine, Base
from app.core.init_db import init_db

# Routers
from app.api.auth import router as auth_router
from app.api.profile import router as profile_router
from app.api.skills import router as skills_router
from app.api.careers import router as careers_router
from app.api.roadmaps import router as roadmaps_router
from app.api.assessments import router as assessments_router
from app.api.resources import router as resources_router
from app.api.mentor import router as mentor_router
from app.api.agents import router as agents_router
from app.api.progress import router as progress_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQLite database and seed initial data automatically
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()
    yield

app = FastAPI(
    title="SkillPath AI - Intelligent Personalized Learning Platform",
    description="Multi-agent educational technology platform featuring skill gap analysis, career readiness matching, adaptive roadmaps, and contextual AI mentoring.",
    version=settings.VERSION,
    lifespan=lifespan
)

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers under /api
api_prefix = settings.API_V1_STR

app.include_router(auth_router, prefix=api_prefix)
app.include_router(profile_router, prefix=api_prefix)
app.include_router(skills_router, prefix=api_prefix)
app.include_router(careers_router, prefix=api_prefix)
app.include_router(roadmaps_router, prefix=api_prefix)
app.include_router(assessments_router, prefix=api_prefix)
app.include_router(resources_router, prefix=api_prefix)
app.include_router(mentor_router, prefix=api_prefix)
app.include_router(agents_router, prefix=api_prefix)
app.include_router(progress_router, prefix=api_prefix)

@app.get("/")
def root():
    return {
        "name": "SkillPath AI API",
        "version": settings.VERSION,
        "status": "operational",
        "docs": "/docs",
        "agents": 6,
        "mode": "competition_ready_deterministic"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
