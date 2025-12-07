"""
Database connection and operations.
Supports both Supabase (production) and demo mode (local JSON).
"""
import os
import json
from dotenv import load_dotenv
from typing import Optional, List, Dict

load_dotenv()

# Check if we're in demo mode
DEMO_MODE = not (os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_KEY"))

# Supabase client singleton
_supabase_client = None

# Demo data cache
_demo_events = None


def _load_demo_events() -> List[Dict]:
    """Load demo events from sources.py."""
    global _demo_events
    if _demo_events is None:
        # Import the curated events from scraper sources
        import sys
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from scraper.sources import ESSENTIAL_EVENTS
        
        # Add mock IDs
        _demo_events = []
        for i, event in enumerate(ESSENTIAL_EVENTS):
            event_copy = event.copy()
            event_copy['id'] = i + 1
            _demo_events.append(event_copy)
    
    return _demo_events


def get_supabase():
    """Get or create Supabase client."""
    global _supabase_client
    
    if DEMO_MODE:
        return None
    
    if _supabase_client is None:
        from supabase import create_client
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        _supabase_client = create_client(url, key)
    
    return _supabase_client


def get_all_events(
    category: str = None,
    importance: int = None,
    year_from: int = None,
    year_to: int = None,
    search: str = None,
    limit: int = 500
) -> List[Dict]:
    """
    Fetch events from database with optional filters.
    Falls back to demo data if Supabase not configured.
    """
    if DEMO_MODE:
        # Use demo data
        events = _load_demo_events()
        
        # Apply filters
        if category:
            events = [e for e in events if e.get('category') == category]
        if importance:
            events = [e for e in events if e.get('importance', 3) >= importance]
        if year_from:
            events = [e for e in events if e.get('year', 0) >= year_from]
        if year_to:
            events = [e for e in events if e.get('year', 9999) <= year_to]
        if search:
            search_lower = search.lower()
            events = [e for e in events if 
                     search_lower in e.get('title', '').lower() or 
                     search_lower in e.get('description', '').lower()]
        
        # Sort by year, month, day
        events = sorted(events, key=lambda x: (
            x.get('year', 0), 
            x.get('month', 0), 
            x.get('day', 0)
        ))
        
        return events[:limit]
    
    # Use Supabase
    supabase = get_supabase()
    query = supabase.table("events").select("*")
    
    if category:
        query = query.eq("category", category)
    if importance:
        query = query.gte("importance", importance)
    if year_from:
        query = query.gte("year", year_from)
    if year_to:
        query = query.lte("year", year_to)
    if search:
        query = query.or_(f"title.ilike.%{search}%,description.ilike.%{search}%")
    
    query = query.order("year", desc=False).order("month", desc=False).order("day", desc=False)
    query = query.limit(limit)
    
    result = query.execute()
    return result.data


def get_event_by_id(event_id: int) -> Optional[Dict]:
    """Fetch a single event by ID."""
    if DEMO_MODE:
        events = _load_demo_events()
        for event in events:
            if event.get('id') == event_id:
                return event
        return None
    
    supabase = get_supabase()
    result = supabase.table("events").select("*").eq("id", event_id).single().execute()
    return result.data


def get_event_stats() -> Dict:
    """Get statistics about events for charts."""
    if DEMO_MODE:
        events = _load_demo_events()
    else:
        supabase = get_supabase()
        result = supabase.table("events").select("year, category, importance").execute()
        events = result.data
    
    # Aggregate by year
    years = {}
    categories = {}
    
    for event in events:
        year = event.get("year")
        category = event.get("category")
        
        if year:
            years[year] = years.get(year, 0) + 1
        if category:
            categories[category] = categories.get(category, 0) + 1
    
    return {
        "total_events": len(events),
        "events_by_year": dict(sorted(years.items())),
        "events_by_category": categories,
        "year_range": {
            "min": min(years.keys()) if years else None,
            "max": max(years.keys()) if years else None
        }
    }


def insert_event(event_data: dict):
    """Insert a new event."""
    if DEMO_MODE:
        raise ValueError("Cannot insert events in demo mode. Configure Supabase first.")
    
    supabase = get_supabase()
    result = supabase.table("events").insert(event_data).execute()
    return result.data


def insert_events_batch(events: list):
    """Insert multiple events at once."""
    if DEMO_MODE:
        raise ValueError("Cannot insert events in demo mode. Configure Supabase first.")
    
    supabase = get_supabase()
    result = supabase.table("events").insert(events).execute()
    return result.data


def is_demo_mode() -> bool:
    """Check if running in demo mode."""
    return DEMO_MODE
