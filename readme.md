# MMA ELO Rating System

An Elo rating system for MMA fighters built on Wikipedia fight data. This project scrapes fighter information and match history from Wikipedia, calculates dynamic Elo ratings adjusting for fighter age and KOs, and provides fighter comparison predictions.

## Prerequisites

- Docker and Docker Compose
- Python 3.7+
- PostgreSQL (via Docker)

## Installation

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment variables (optional - defaults provided):
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials if needed
   ```

## Setting Up

1. Make sure docker is running
2. Open the terminal and navigate to the project folder.
3. Run the command `docker-compose up`.
4. Open another terminal window and execute the following commands:
    - `python reset_elos.py`
    - `python compute_elos.py`

## Querying

1. Complete the `query.txt` file with the provided template for fighters.
2. Run the command `python query.py` to execute the query.

## Other commands

- To generate setup files for the SQL database, run `python generate_dump_sql.py`.
- To rescrape the data, ensure that you truncate the tables and then run `python scrape.py`.

## Project Structure

- **Config/** - Configuration constants (ELO multipliers, penalties, etc.)
- **DB/** - Database layer (PostgreSQL client, models for Fighters/Fights/EloChanges)
- **ELO/** - Elo calculation logic (EloCalculator, EloHelper, StatsHelper)
- **WikiScraper/** - Web scraping components for Wikipedia fighter data
- **FighterQueue/** - Queue for managing fighter URLs during scraping
- **Helpers/** - Utility modules (date handling)
- **Querier/** - Query processing for fighter comparisons
- **SQL/** - Database schema and initialization scripts

## How It Works

1. **Scraping**: `scrape.py` extracts fighter data and fight records from Wikipedia
2. **ELO Calculation**: `compute_elos.py` processes fights chronologically and updates ratings
   - Adjusts for fighter age and KO outcomes
   - Starting rating: 1500
3. **Predictions**: `query.py` provides win probability for fighter matchups

## Troubleshooting

If you encounter any issues, follow these steps:

1. Delete the `data` folder.
2. Rebuild the Docker container.
   - If the issue persists, repeat from the first step but also delete `SQL/fighters.sql` and `SQL/fights.sql` before rebuilding container.
3. Rescrape the data by running the appropriate commands (check "Other commands" section).
