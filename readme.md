# Project Name

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

## Troubleshooting

If you encounter any issues, follow these steps:

1. Delete the `data` folder.
2. Rebuild the Docker container.
   - If the issue persists, repeat from the first step but also delete `SQL/fighters.sql` and `SQL/fights.sql` before rebuilding container.
3. Rescrape the data by running the appropriate commands (check "Other commands" section).
