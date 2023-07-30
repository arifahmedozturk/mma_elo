import json
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
dump_to_query = False
query = []
if "-q" in sys.argv:
    dump_to_query  = True
print("queyr dumop", dump_to_query)
for match in matches:
    if dump_to_query:
        query.append([match['fighter'], match['opponent']])
    else:
        FightDB.add_fight(match['fighter'], match['opponent'], match['result'], match['date'], match['method'], match['event'])

    print(f"Added fight: {match['fighter']} VS. {match['opponent']} - {match['method']}")

if dump_to_query:
    with open("query.txt", "w", encoding="utf-8") as file:
        file.write(json.dumps(query, indent=4, ensure_ascii=False))
        file.close()
    print("Dumped to query.txt")