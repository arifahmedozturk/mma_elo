from WikiScraper.WikiScraper import WikiScraper
from FighterQueue.FighterQueue import FighterQueue
from DB import Fight, Fighter

FighterDB = Fighter.Fighter()
FightDB = Fight.Fight()

fighter_queue = FighterQueue()
fighter_queue.insert('https://en.wikipedia.org/wiki/Syuri')
fighter_queue.insert('https://en.wikipedia.org/wiki/Jon_Jones')

wiki_scraper = WikiScraper()

while True:
    fighter_url = fighter_queue.pop()
    print("Started at url", fighter_url)
    if fighter_url is None:
        break

    fighter_name = wiki_scraper.get_fighter_name(fighter_url)
    if fighter_name is None:
        print("name not found, skipping")
        continue
    if FighterDB.get_fighter(fighter_name) is not None:
        print("Found redirect, skipping")
        continue
    fighter_dob = wiki_scraper.get_fighter_dob(fighter_url)
    matches = wiki_scraper.get_matches(fighter_url)
    opponent_urls = wiki_scraper.get_opponent_urls(fighter_url)
    for match in matches:
        ufc_texts = ["UFC", "The Ultimate Fighter"]
        ufc_match = False
        for ufc_text in ufc_texts:
            if ufc_text in match['event']:
                ufc_match = True
                break
        if ufc_match:
            opponent_url = opponent_urls.get(match['opponent'])
            if(opponent_url is None):
                continue
            fighter_queue.insert(opponent_url)
    
    FighterDB.add_fighter(fighter_name, fighter_dob)
    for match in matches:
        FightDB.add_fight(fighter_name, match['opponent'], match['result'], match['date'], match['method'], match['event'])
    print("Finished adding", fighter_name, "; added", str(len(matches)), "fights")
