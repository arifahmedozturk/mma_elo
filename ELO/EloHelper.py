import math
from datetime import datetime
from Config.Config import Config

class EloHelper:
    def __init__(self):
         self.config = Config()
    
    def get_result_score(self, result, method_of_victory):
        if(result != "Win" and result != "Loss"):
            return 0.5, 0.5
        
        if result == "Win":
            if "Decision (split)" in method_of_victory:
                return 0.67, 0.33
            return 1, 0
        
        if "Decision (split)" in method_of_victory:
                return 0.33, 0.67
        return 0, 1

    def get_age_penalty(self, dob, last_age_penalty, fight_date):
        def get_year_difference(dateString1, dateString2):
            date1 = datetime.strptime(dateString1, "%Y-%m-%d")
            date2 = datetime.strptime(dateString2, "%Y-%m-%d")

            year_difference = date2.year - date1.year
            if (date2.month, date2.day) < (date1.month, date1.day):
                year_difference -= 1

            return year_difference
        
        if dob is None:
            return 0
        
        age_at_penalty = get_year_difference(dob, last_age_penalty)
        age_at_fight = get_year_difference(dob, fight_date)

        if age_at_fight < self.config.MIN_AGE_FOR_PENALTY:
            return 0
        
        return -1*self.config.AGE_PENALTY*(age_at_fight - max(self.config.MIN_AGE_FOR_PENALTY, age_at_penalty))

    def get_result_penalty(self, result, method_of_victory):
        if result == "Win" and "KO" in method_of_victory:
            return 0, -1*self.config.KO_PENALTY
            
        if result == "Loss" and "KO" in method_of_victory:
            return -1*self.config.KO_PENALTY, 0
        
        return 0, 0

    def get_elo_changes(self, fighter, opponent, fight):
        fighter_age_penalty = self.get_age_penalty(fighter['dob'], fighter['last_age_penalty'], fight['date'])
        opponent_age_penalty = self.get_age_penalty(opponent['dob'], opponent['last_age_penalty'], fight['date'])

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