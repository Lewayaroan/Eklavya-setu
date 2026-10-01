"""
FastAPI application entry point for Eklavya Setu.
Smart India Hackathon 2026 • SIH26238 • Ministry of Tribal Affairs (MoTA)
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.database import Base, engine, SessionLocal, seed_initial_data
from backend.routers import scholarships, jago_ai, outreach_radar

# Initialize database schema and seed initial data
Base.metadata.create_all(bind=engine)
db = SessionLocal()
try:
    seed_initial_data(db)
finally:
    db.close()

app = FastAPI(
    title="Eklavya Setu API",
    description="Unified Tribal Scholarship Portal & JAGO AI Voice Assistant • Ministry of Tribal Affairs (MoTA)",
    version="1.0.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(scholarships.router)
app.include_router(jago_ai.router)
app.include_router(outreach_radar.router)

# Locate frontend directory
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
ROOT_INDEX = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "index.html")

if os.path.exists(FRONTEND_DIR):
    app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Eklavya Setu API",
        "ministry": "Ministry of Tribal Affairs (MoTA)",
        "sih_code": "SIH26238",
    }


@app.get("/")
def serve_root():
    if os.path.exists(ROOT_INDEX):
        return FileResponse(ROOT_INDEX)
    if os.path.exists(os.path.join(FRONTEND_DIR, "index.html")):
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))
    return {"message": "Eklavya Setu Backend Running. Open /docs for Swagger API documentation."}
