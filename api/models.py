"""
Pydantic models for API request/response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class EventCategory(str, Enum):
    """Categories for AI events."""
    RESEARCH = "research"           # Academic papers, breakthroughs
    MODEL = "model"                 # AI model releases (GPT, Claude, etc.)
    COMPANY = "company"             # Company founded, acquired, etc.
    PRODUCT = "product"             # Product launches, integrations
    HARDWARE = "hardware"           # GPUs, TPUs, chips
    REGULATION = "regulation"       # Laws, policies
    MILESTONE = "milestone"         # Notable achievements
    OTHER = "other"


class EventBase(BaseModel):
    """Base event model with common fields."""
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = Field(None, max_length=5000)
    year: int = Field(..., ge=1940, le=2030)
    month: Optional[int] = Field(None, ge=1, le=12)
    day: Optional[int] = Field(None, ge=1, le=31)
    category: EventCategory
    importance: int = Field(3, ge=1, le=5)  # 1=minor, 5=major
    source_url: Optional[str] = None
    image_url: Optional[str] = None


class EventCreate(EventBase):
    """Model for creating a new event."""
    pass


class EventResponse(EventBase):
    """Model for event API responses."""
    id: int
    
    class Config:
        from_attributes = True


class EventsListResponse(BaseModel):
    """Response model for list of events."""
    events: List[EventResponse]
    total: int
    

class StatsResponse(BaseModel):
    """Response model for statistics."""
    total_events: int
    events_by_year: dict
    events_by_category: dict
    year_range: dict


class FilterParams(BaseModel):
    """Query parameters for filtering events."""
    category: Optional[EventCategory] = None
    importance: Optional[int] = Field(None, ge=1, le=5)
    year_from: Optional[int] = Field(None, ge=1940)
    year_to: Optional[int] = Field(None, le=2030)
    search: Optional[str] = None
    limit: int = Field(500, ge=1, le=1000)
