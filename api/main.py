"""
AI Evolution Atlas - FastAPI Application
Main API routes and application setup.
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import Optional
import os

from .models import EventCategory, EventResponse, StatsResponse
from . import database as db

# Create FastAPI app
app = FastAPI(
    title="AIONOS",
    description="The Eternal AI Timeline - Interactive history of AI and milestones",
    version="1.0.0"
)

# Get the directory where this file is located
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")


# Mount static files (CSS, JS)
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
async def root():
    """Serve the main HTML page."""
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "AI Evolution Atlas API", "docs": "/docs"}


@app.get("/api/events")
async def get_events(
    category: Optional[EventCategory] = Query(None, description="Filter by category"),
    importance: Optional[int] = Query(None, ge=1, le=5, description="Minimum importance (1-5)"),
    year_from: Optional[int] = Query(None, ge=1940, description="Start year"),
    year_to: Optional[int] = Query(None, le=2030, description="End year"),
    search: Optional[str] = Query(None, description="Search in title/description"),
    limit: int = Query(500, ge=1, le=1000, description="Max results")
):
    """
    Get all AI events with optional filters.
    
    - **category**: Filter by event type (research, model, company, etc.)
    - **importance**: Minimum importance level (1=minor, 5=major)
    - **year_from/year_to**: Filter by year range
    - **search**: Full-text search in title and description
    """
    try:
        events = db.get_all_events(
            category=category.value if category else None,
            importance=importance,
            year_from=year_from,
            year_to=year_to,
            search=search,
            limit=limit
        )
        return {"events": events, "total": len(events)}
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/api/events/{event_id}")
async def get_event(event_id: int):
    """Get a single event by ID."""
    try:
        event = db.get_event_by_id(event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        return event
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/api/stats", response_model=StatsResponse)
async def get_stats():
    """
    Get statistics about AI events.
    
    Returns counts by year and category for charts.
    """
    try:
        stats = db.get_event_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/api/categories")
async def get_categories():
    """Get list of all event categories."""
    return {
        "categories": [
            {"value": cat.value, "label": cat.value.title()} 
            for cat in EventCategory
        ]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for deployment."""
    return {
        "status": "healthy", 
        "service": "aionos",
        "demo_mode": db.is_demo_mode()
    }
