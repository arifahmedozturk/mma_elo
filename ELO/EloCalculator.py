import json
from ELO.EloHelper import EloHelper
from DB.Fight import Fight
from DB.Fighter import Fighter

class EloCalculator:
    def __init__(self):
        self.helper = EloHelper()
        self.FightDB = Fight()
        self.FighterDB = Fighter()
    
    def save_last_date(self, fight_date):
        with open("last_date.txt", "w") as file:
            file.write(json.dumps(fight_date))

    def load_last_date(self):
        with open("last_date.txt", "r") as file:
            return (json.loads(file.read()))
    
    def remove_duplicate_matches(self, matches):
        existing_matches = {}
        unique_matches = []
        for match in matches:
            if existing_matches.get(match['fighter'] + "+" + match['opponent']) is None:
                existing_matches[match['fighter'] + "+" + match['opponent']] = True
                existing_matches[match['opponent'] + "+" + match['fighter']] = False
                unique_matches.append(match)
        return unique_matches
    
    def start_elo_computation(self):
        for x in range(10000):
            last_date = self.load_last_date()
            closest_date = self.FightDB.get_closest_date_to_date(last_date)
            if closest_date is None:
                break
            self.save_last_date(closest_date)

            fights = self.remove_duplicate_matches(self.FightDB.get_fights_at_date(closest_date))
            print("At ", closest_date)
            print("Found", len(fights), "fights")
            for fight in fights:
                if 'UFC' not in fight['event'] and 'The Ultimate Fighter' not in fight['event']:
                    print("Not UFC fight, skipping...")
                    continue
                fighter = self.FighterDB.get_fighter(fight['fighter'])
                opponent = self.FighterDB.get_fighter(fight['opponent'])

                fighter_delta_elo, opponent_delta_elo = self.helper.get_elo_changes(fighter, opponent, fight)
                self.FighterDB.set_fighter_elo(fighter['name'], fighter['elo'] + fighter_delta_elo)
                self.FighterDB.set_fighter_last_age_penalty(fighter['name'], fight['date'])
                self.FighterDB.set_fighter_elo(opponent['name'], opponent['elo'] + opponent_delta_elo)
                self.FighterDB.set_fighter_last_age_penalty(opponent['name'], fight['date'])