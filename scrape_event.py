from WikiScraper.WikiScraper import WikiScraper
from DB import Fight

FightDB = Fight.Fight()

wiki_scraper = WikiScraper()
matches = wiki_scraper.get_event_matches('https://en.wikipedia.org/wiki/UFC_290')
for match in matches:
    FightDB.add_fight(match['fighter'], match['opponent'], match['result'], match['date'], match['method'], match['event'])
    print(f"Added fight: {match['fighter']} VS. {match['opponent']} - {match['method']}")