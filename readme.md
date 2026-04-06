# MMA ELO Rating System

An Elo rating system for UFC fighters built on Wikipedia fight data. The scraper crawls fighter pages recursively from a set of seed fighters, and the rating system adjusts for fighter age decline and KO stoppages on top of standard Elo.

## Top 30 Fighters by Elo

| Rank | Fighter | Elo |
|------|---------|-----|
| 1 | Islam Makhachev | 2738 |
| 2 | Jon Jones | 2651 |
| 3 | Georges St-Pierre | 2572 |
| 4 | Khabib Nurmagomedov | 2533 |
| 5 | Ilia Topuria | 2468 |
| 6 | Charles Oliveira | 2449 |
| 7 | Khamzat Chimaev | 2442 |
| 8 | Merab Dvalishvili | 2439 |
| 9 | Francis Ngannou | 2435 |
| 10 | Petr Yan | 2404 |
| 11 | Valentina Shevchenko | 2375 |
| 12 | Alexander Volkanovski | 2352 |
| 13 | Movsar Evloev | 2333 |
| 14 | Max Holloway | 2299 |
| 15 | Justin Gaethje | 2292 |
| 16 | Kamaru Usman | 2289 |
| 17 | Demetrious Johnson | 2287 |
| 18 | Arman Tsarukyan | 2272 |
| 19 | Alex Pereira | 2260 |
| 20 | Nassourdine Imavov | 2255 |
| 21 | Dricus du Plessis | 2251 |
| 22 | Amanda Nunes | 2248 |
| 23 | Belal Muhammad | 2241 |
| 24 | Aljamain Sterling | 2237 |
| 25 | Shavkat Rakhmonov | 2233 |
| 26 | Ian Machado Garry | 2231 |
| 27 | Michael Morales | 2216 |
| 28 | Zhang Weili | 2212 |
| 29 | Umar Nurmagomedov | 2209 |
| 30 | Ciryl Gane | 2200 |

## Rating Formula

This system extends standard Elo with two adjustments specific to combat sports.

### Standard Elo

Each fight updates both fighters' ratings:

```
new_rating = old_rating + K × (actual_score − expected_score)
```

Where:
- `K = 200` (controls how much a single fight moves the rating)
- `expected_score = 10^(rating/800) / (10^(rating_A/800) + 10^(rating_B/800))`
- `actual_score` = 1 for a win, 0 for a loss, 0.5 for a draw or no-contest, 0.67/0.33 for a split decision win/loss

### Age Penalty

Fighters older than 38 lose **50 Elo points per year** of age past that threshold, applied at the time of each fight. This reflects the well-documented performance decline in combat sports past that age and prevents older fighters from holding inflated ratings built up earlier in their career.

### KO Penalty

A fighter who is knocked out or TKO'd loses an **extra 25 points** on top of the standard Elo loss. This accounts for the accumulated physical damage from a KO — a fighter who has been stopped is more likely to carry lasting effects into future fights. The winner receives no bonus; only the loser is penalised.

### Win Probability

Given two fighters' ratings, the predicted win probability is:

```
P(A beats B) = 1 / (1 + 10^((rating_B − rating_A) / 800))
```

All fighters start at **1500**.

## Prerequisites

- Docker and Docker Compose
- Python 3.7+

## Installation

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy the environment file:
   ```bash
   cp .env.example .env
   ```

## Setting Up

1. Make sure Docker is running.
2. Start the database:
   ```bash
   docker compose up -d
   ```
3. Reset state and compute ratings:
   ```bash
   python reset_elos.py
   python compute_elos.py
   ```

## Scraping

The scraper starts from Jon Jones and Syuri as seed fighters and crawls all UFC opponents recursively:

```bash
python scrape.py
```

Edit the `fighter_queue.insert(...)` calls in `scrape.py` to change the starting fighters.

## Querying

Create a `query.txt` file with a JSON array of fighter pairs:

```json
[
    ["Jon Jones", "Stipe Miocic"],
    ["Israel Adesanya", "Alex Pereira"]
]
```

Then run:
```bash
python query.py
```

Results (win probabilities and odds) are written to `query_answer.txt`.

## Other Commands

- `python generate_dump_sql.py` — exports the current database to `SQL/fighters.sql` and `SQL/fights.sql`
- `python reset_elos.py` — resets all ratings to 1500 (run before recomputing)

## Project Structure

```
Config/         Configuration constants (K-factor, penalties, starting Elo)
DB/             PostgreSQL client and models (Fighter, Fight, EloChange)
ELO/            Rating logic (EloCalculator, EloHelper, StatsHelper)
WikiScraper/    Wikipedia scraper and HTML parsing components
FighterQueue/   BFS queue for crawling opponent pages
Helpers/        Date utilities
Querier/        Win probability calculator
SQL/            Database schema
tests/          Unit tests
```

## Troubleshooting

If you get a database error on startup, the most likely cause is a stale `data/` volume. Delete it and restart:

```bash
docker compose down
rm -rf data/
docker compose up -d
```

If that doesn't work, also delete `SQL/fighters.sql` and `SQL/fights.sql` before restarting.
