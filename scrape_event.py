import sys
from WikiScraper.WikiScraper import WikiScraper
from DB import Fight

if len(sys.argv) < 2:
    raise Exception("Event URL not provided")
url = sys.argv[1]

if 'https://en.wikipedia.org/wiki/' not in url:
    raise Exception("URL is not valid")

FightDB = Fight.Fight()

wiki_scraper = WikiScraper()
matches = wiki_scraper.get_event_matches(url)
for match in matches:
    FightDB.add_fight(match['fighter'], match['opponent'], match['result'], match['date'], match['method'], match['event'])
    print(f"Added fight: {match['fighter']} VS. {match['opponent']} - {match['method']}")
