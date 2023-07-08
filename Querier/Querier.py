import json
import math
from DB.Fighter import Fighter

class Querier:
    def __init__(self):
        self.matches = self.read_query()
        self.FighterDB = Fighter()
    
    def read_query(self):
        with open("query.txt", "r", encoding="utf-8") as f:
            matches = json.loads(f.read())
            return matches
    
    def get_fighters_from_fight(self, fight):
        fighter_name = fight[0]
        opponent_name = fight[1]

        fighter = self.FighterDB.get_fighter(fighter_name)
        opponent = self.FighterDB.get_fighter(opponent_name)
        return fighter, opponent
    
    def pretty_print_fight(self, fighter, opponent):
        print_text = f"{fighter['name']}({fighter['elo']}) VS. {opponent['name']}({opponent['elo']})" + "\n"
        
        fighter_win_probability = 1 / (1 + math.pow(10, (opponent['elo'] - fighter['elo'])/400))
        opponent_win_probability = 1 / (1 + math.pow(10, (fighter['elo'] - opponent['elo'])/400))
        print_text += f"Probabilities: {round(fighter_win_probability, 2)} - {round(opponent_win_probability, 2)}" + "\n"
 
        fighter_odd = 1 / fighter_win_probability
        opponent_odd = 1 / opponent_win_probability
        print_text += f"Odds: {round(fighter_odd, 2)} - {round(opponent_odd, 2)}" + "\n"
        print_text += "\n"
        return print_text
    
    def process_query(self):
        print_text = ""
        for match in self.matches:
            fighter, opponent = self.get_fighters_from_fight(match)
            print_text += self.pretty_print_fight(fighter, opponent)
        with open("query_answer.txt", "w", encoding="utf-8") as f:
            f.write(print_text)
