"""
Script to populate Supabase database with scraped events.
Run this after setting up your Supabase project.
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper.scraper import run_scraper, load_raw_data
from api.database import get_supabase, insert_events_batch


def populate_database(use_cache: bool = True):
    """
    Run the scraper and populate the Supabase database.
    """
    print("=" * 50)
    print("AI Evolution Atlas - Database Population")
    print("=" * 50)
    
    # Get events (from cache or fresh scrape)
    events = run_scraper(use_cache=use_cache)
    
    if not events:
        print("No events to insert!")
        return
    
    print(f"\nPreparing to insert {len(events)} events to Supabase...")
    
    try:
        # Insert in batches of 50 to avoid timeout
        batch_size = 50
        for i in range(0, len(events), batch_size):
            batch = events[i:i + batch_size]
            insert_events_batch(batch)
            print(f"  Inserted batch {i // batch_size + 1}/{(len(events) - 1) // batch_size + 1}")
        
        print(f"\n✅ Successfully inserted {len(events)} events!")
        
    except Exception as e:
        print(f"\n❌ Error inserting events: {e}")
        print("\nMake sure you have:")
        print("1. Created the 'events' table in Supabase")
        print("2. Set SUPABASE_URL and SUPABASE_KEY in .env")
        raise


def main():
    """Entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Populate Supabase with AI events")
    parser.add_argument("--fresh", action="store_true", help="Force fresh scrape (don't use cache)")
    args = parser.parse_args()
    
    populate_database(use_cache=not args.fresh)


if __name__ == "__main__":
    main()
