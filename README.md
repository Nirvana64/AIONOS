# AIONOS

> *From Greek "Aion" = eternal age — Timeless Intelligence spanning ages*

An interactive timeline tracking the evolution of Artificial Intelligence from 1950 to present day.

## Features

- Interactive timeline of 50+ AI milestones
- Filter by category (Research, Models, Companies, Products, Regulation)
- Light/Dark mode toggle
- Key statistics overview
- Automated data collection via web scraping
- Demo mode works without database setup

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI (Python) |
| Database | Supabase (PostgreSQL) |
| Frontend | HTML, CSS, Vanilla JavaScript |
| Scraping | BeautifulSoup, Requests |

## Quick Start

```bash
# Clone and setup
git clone https://github.com/Nirvana64/AIONOS.git
cd AIONOS

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run the server
python run.py
```

Open **http://localhost:8000** in your browser.

## Project Structure

```
AIONOS/
├── api/
│   ├── main.py          # FastAPI routes and server
│   ├── database.py      # Supabase connection + demo mode
│   └── models.py        # Pydantic data schemas
├── scraper/
│   ├── sources.py       # Curated AI events data
│   ├── scraper.py       # Wikipedia scraping logic
│   └── populate_db.py   # Database population script
├── static/
│   ├── index.html       # Main HTML page
│   ├── css/style.css    # Styling with light/dark themes
│   └── js/app.js        # Frontend interactivity
├── database_schema.sql  # SQL to create Supabase table
├── requirements.txt     # Python dependencies
└── run.py               # Entry point
```

## Optional: Connect Supabase

1. Create account at [supabase.com](https://supabase.com)
2. Create new project
3. Run `database_schema.sql` in SQL Editor
4. Copy URL and anon key to `.env`:
   ```
   SUPABASE_URL=your_project_url
   SUPABASE_KEY=your_anon_key
   ```
5. Populate database: `python -m scraper.populate_db`

## License

MIT
