"""
Web scraper for AI history events.
Scrapes Wikipedia and other sources for AI timeline data.
"""
import requests
from bs4 import BeautifulSoup
import re
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from .sources import WIKIPEDIA_SOURCES, ESSENTIAL_EVENTS, CATEGORY_KEYWORDS

# Directory for raw scraped data
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw")


def ensure_data_dir():
    """Create data directory if it doesn't exist."""
    os.makedirs(DATA_DIR, exist_ok=True)


def fetch_page(url: str) -> Optional[BeautifulSoup]:
    """Fetch and parse a webpage."""
    headers = {
        "User-Agent": "AIEvolutionAtlas/1.0 (Educational Project; https://github.com/example)"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return BeautifulSoup(response.content, "html5lib")
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def parse_year_from_text(text: str) -> Optional[int]:
    """Extract a year (1900-2030) from text."""
    match = re.search(r'\b(19\d{2}|20[0-2]\d)\b', text)
    if match:
        return int(match.group(1))
    return None


def guess_category(text: str) -> str:
    """Guess event category based on keywords in text."""
    text_lower = text.lower()
    
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                return category
    
    return "other"


def guess_importance(text: str) -> int:
    """Estimate importance based on text content."""
    text_lower = text.lower()
    
    # High importance indicators
    high_importance = ["first", "breakthrough", "revolutionary", "landmark", "major", 
                       "world champion", "billion", "transformer", "gpt", "chatgpt"]
    
    # Medium importance indicators  
    medium_importance = ["introduced", "released", "launched", "new", "improved"]
    
    for word in high_importance:
        if word in text_lower:
            return 5
    
    for word in medium_importance:
        if word in text_lower:
            return 3
    
    return 2


def scrape_wikipedia_timeline(url: str) -> List[Dict]:
    """
    Scrape events from a Wikipedia timeline page.
    These typically have tables with Year, Event structure.
    """
    soup = fetch_page(url)
    if not soup:
        return []
    
    events = []
    
    # Look for tables with timeline data
    tables = soup.find_all("table", class_="wikitable")
    
    for table in tables:
        rows = table.find_all("tr")
        current_year = None
        
        for row in rows:
            cells = row.find_all(["td", "th"])
            if not cells:
                continue
            
            # Try to extract year from first cell
            first_cell = cells[0].get_text(strip=True)
            year = parse_year_from_text(first_cell)
            if year:
                current_year = year
            
            # Get event text from remaining cells
            if len(cells) > 1:
                event_text = cells[-1].get_text(strip=True)
                
                # Skip header rows and very short entries
                if len(event_text) < 20 or event_text.lower().startswith("year"):
                    continue
                    
                if current_year:
                    # Create a title from the first sentence or portion
                    title = event_text[:200].split('.')[0]
                    if len(title) > 150:
                        title = title[:147] + "..."
                    
                    events.append({
                        "year": current_year,
                        "title": title,
                        "description": event_text[:1000],
                        "category": guess_category(event_text),
                        "importance": guess_importance(event_text),
                        "source_url": url
                    })
    
    # Also look for timeline lists (dl/dt/dd structure)
    dls = soup.find_all("dl")
    for dl in dls:
        dts = dl.find_all("dt")
        dds = dl.find_all("dd")
        
        for dt in dts:
            year = parse_year_from_text(dt.get_text())
            if year:
                # Find corresponding dd elements
                next_element = dt.find_next_sibling()
                while next_element and next_element.name == "dd":
                    text = next_element.get_text(strip=True)
                    if len(text) > 20:
                        title = text[:200].split('.')[0]
                        events.append({
                            "year": year,
                            "title": title[:150],
                            "description": text[:1000],
                            "category": guess_category(text),
                            "importance": guess_importance(text),
                            "source_url": url
                        })
                    next_element = next_element.find_next_sibling()
    
    return events


def scrape_all_sources() -> List[Dict]:
    """Scrape all configured Wikipedia sources."""
    all_events = []
    
    for source in WIKIPEDIA_SOURCES:
        print(f"Scraping: {source['name']}...")
        events = scrape_wikipedia_timeline(source['url'])
        print(f"  Found {len(events)} events")
        all_events.extend(events)
    
    return all_events


def merge_with_essential_events(scraped_events: List[Dict]) -> List[Dict]:
    """
    Merge scraped events with essential curated events.
    Essential events take priority if there's overlap.
    """
    # Create a set of (year, title_start) for deduplication
    essential_keys = set()
    for event in ESSENTIAL_EVENTS:
        key = (event['year'], event['title'][:30].lower())
        essential_keys.add(key)
    
    # Filter scraped events that overlap with essential ones
    filtered_scraped = []
    for event in scraped_events:
        key = (event['year'], event['title'][:30].lower())
        if key not in essential_keys:
            filtered_scraped.append(event)
    
    # Combine and sort by year
    all_events = ESSENTIAL_EVENTS + filtered_scraped
    all_events.sort(key=lambda x: (x['year'], x.get('month', 0), x.get('day', 0)))
    
    return all_events


def save_raw_data(events: List[Dict], filename: str = "scraped_events.json"):
    """Save scraped data to JSON for review."""
    ensure_data_dir()
    filepath = os.path.join(DATA_DIR, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(events, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(events)} events to {filepath}")
    return filepath


def load_raw_data(filename: str = "scraped_events.json") -> List[Dict]:
    """Load previously scraped data."""
    filepath = os.path.join(DATA_DIR, filename)
    
    if not os.path.exists(filepath):
        return []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def run_scraper(use_cache: bool = True) -> List[Dict]:
    """
    Main scraper entry point.
    
    Args:
        use_cache: If True, skip scraping if data file exists
    """
    cache_file = os.path.join(DATA_DIR, "scraped_events.json")
    
    if use_cache and os.path.exists(cache_file):
        print("Using cached scraped data...")
        scraped = load_raw_data()
    else:
        print("Starting web scraper...")
        scraped = scrape_all_sources()
        save_raw_data(scraped, "scraped_events.json")
    
    # Merge with essential events
    all_events = merge_with_essential_events(scraped)
    save_raw_data(all_events, "all_events.json")
    
    print(f"\nTotal events after merge: {len(all_events)}")
    return all_events


if __name__ == "__main__":
    events = run_scraper(use_cache=False)
    print(f"\nSample events:")
    for event in events[:5]:
        print(f"  {event['year']}: {event['title'][:60]}...")
