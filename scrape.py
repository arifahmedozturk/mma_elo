import concurrent.futures
from threading import Lock
from WikiScraper.WikiScraper import WikiScraper
from DB import Fight, Fighter

NUM_WORKERS = 10
UFC_FILTERS = ["UFC", "The Ultimate Fighter"]

insert_lock = Lock()


def process_fighter(fighter_url):
    """
    Scrape one fighter page. Returns a list of opponent URLs to enqueue.
    Each call gets its own DB connections and WikiScraper (not thread-safe to share).
    """
    wiki_scraper = WikiScraper()
    FighterDB = Fighter.Fighter()
    FightDB = Fight.Fight()

    fighter_name = wiki_scraper.get_fighter_name(fighter_url)
    if fighter_name is None:
        print(f"[skip] name not found: {fighter_url}")
        return []

    # Fast check before acquiring the lock
    if FighterDB.get_fighter(fighter_name, False) is not None:
        print(f"[skip] already exists: {fighter_name}")
        return []

    fighter_dob = wiki_scraper.get_fighter_dob(fighter_url)
    matches = wiki_scraper.get_matches(fighter_url)
    opponent_urls = wiki_scraper.get_opponent_urls(fighter_url)

    new_urls = [
        opponent_urls[match['opponent']]
        for match in matches
        if any(t in match['event'] for t in UFC_FILTERS)
        and match['opponent'] in opponent_urls
    ]

    with insert_lock:
        # Double-check inside the lock to guard against races
        if FighterDB.get_fighter(fighter_name, False) is not None:
            return new_urls
        FighterDB.add_fighter(fighter_name, fighter_dob)
        for match in matches:
            FightDB.add_fight(
                fighter_name, match['opponent'], match['result'],
                match['date'], match['method'], match['event']
            )

    print(f"[done] {fighter_name} — {len(matches)} fights")
    return new_urls


def main():
    seeds = [
        'https://en.wikipedia.org/wiki/Syuri',
        'https://en.wikipedia.org/wiki/Jon_Jones',
    ]

    visited = set(seeds)

    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        # Submit seed fighters
        pending = {executor.submit(process_fighter, url): url for url in seeds}

        while pending:
            done, _ = concurrent.futures.wait(
                pending, return_when=concurrent.futures.FIRST_COMPLETED
            )
            for future in done:
                del pending[future]
                try:
                    for url in future.result():
                        if url not in visited:
                            visited.add(url)
                            f = executor.submit(process_fighter, url)
                            pending[f] = url
                except Exception as e:
                    print(f"[error] {e}")


if __name__ == '__main__':
    main()
