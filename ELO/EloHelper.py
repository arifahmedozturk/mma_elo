import math
from Config.Config import Config
from Helpers.DateHelper import DateHelper
from DB.Fighter import Fighter

class EloHelper:
    def __init__(self):
         self.config = Config()
         self.date_helper = DateHelper()
         self.FighterDB = Fighter()
    
    def get_result_score(self, result, method_of_victory):
        if(result != "Win" and result != "Loss"):
            return 0.5, 0.5
        
        if result == "Win":
            inverse_scores = self.get_result_score("Loss", method_of_victory)
            return inverse_scores[1], inverse_scores[0]
        
        if "Decision (split)" in method_of_victory:
                return 0.33, 0.67
        return 0, 1

    def get_age_penalty_and_new_date(self, last_age_penalty_date, fight_date):
        age_penalty = 0
        penalty_date = last_age_penalty_date
        while fight_date >= penalty_date:
           age_penalty += 50
           penalty_date = self.date_helper.add_years_to_date(penalty_date, 1)
        
        return (-1)*age_penalty, penalty_date
              
    def get_result_penalty(self, result, method_of_victory):
        if result == "Win" and "KO" in method_of_victory:
            return 0, -1*self.config.KO_PENALTY
            
        if result == "Loss" and "KO" in method_of_victory:
            return -1*self.config.KO_PENALTY, 0
        
        return 0, 0

    def get_elo_changes(self, fighter, opponent, fight):
        fighter_age_penalty, fighter_age_penalty_date = self.get_age_penalty_and_new_date(fighter['last_age_penalty'], fight['date'])
        opponent_age_penalty, opponent_age_penalty_date= self.get_age_penalty_and_new_date(opponent['last_age_penalty'], fight['date'])
        self.FighterDB.set_fighter_last_age_penalty(fighter['name'], fighter_age_penalty_date)
        self.FighterDB.set_fighter_last_age_penalty(opponent['name'], opponent_age_penalty_date)

        fighter_elo = fighter['elo'] + fighter_age_penalty
        opponent_elo = opponent['elo'] + opponent_age_penalty

        fighter_transformed_elo = math.pow(10, fighter_elo / self.config.ELO_MULTIPLIER)
        opponent_transformed_elo = math.pow(10, opponent_elo / self.config.ELO_MULTIPLIER)

        fighter_expected_score = fighter_transformed_elo / (fighter_transformed_elo + opponent_transformed_elo)
        opponent_expected_score = opponent_transformed_elo / (fighter_transformed_elo + opponent_transformed_elo)

        fighter_result_score, opponent_result_score = self.get_result_score(fight['result'], fight['method'])
        fighter_result_penalty, opponent_result_penalty = self.get_result_penalty(fight['result'], fight['method'])

        fighter_new_elo = int(fighter_elo + fighter_result_penalty + self.config.ELO_MULTIPLIER * (fighter_result_score - fighter_expected_score))
        opponent_new_elo = int(opponent_elo + opponent_result_penalty + self.config.ELO_MULTIPLIER * (opponent_result_score - opponent_expected_score))

        return fighter_new_elo - fighter['elo'], opponent_new_elo - opponent['elo']