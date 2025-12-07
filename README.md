# AIONOS

> *From Greek "Aion" = eternal age — Timeless Intelligence spanning ages*

An interactive timeline tracking the evolution of Artificial Intelligence from early history to present day.

## Features

- 📅 Interactive timeline of AI milestones
- 🔍 Filter by category (Research, Models, Companies, etc.)
- 🌓 Light/Dark mode toggle
- 📊 Key statistics and trends
- 🤖 Automated data collection via web scraping

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: Supabase (PostgreSQL)
- **Frontend**: HTML + CSS + Vanilla JavaScript
- **Scraping**: BeautifulSoup + Requests

## Setup

### 1. Install Dependencies

```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Configure Supabase

Create a `.env` file with your Supabase credentials:

```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

### 3. Run the Scraper (Optional)

```bash
python -m scraper.main
```

### 4. Start the Server

```bash
python run.py
```

Visit `http://localhost:8000` in your browser.

## Project Structure

```
ai_atlas/
├── api/            # FastAPI backend
├── scraper/        # Web scraping modules
├── static/         # Frontend files (HTML, CSS, JS)
├── data/           # Raw scraped data
├── requirements.txt
└── run.py          # Entry point
```

## License

MIT
