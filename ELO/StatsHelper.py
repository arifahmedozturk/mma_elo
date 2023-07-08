class StatsHelper:
    def __init__(self):
        self.total_predictions = 0
        self.correct_predictions = 0
    
    def log_positive_answer(self):
        self.correct_predictions += 1
        self.total_predictions += 1
    
    def log_negative_answer(self):
        self.total_predictions += 1

    def log_fight(self, fighter, opponent, fight):
        if fighter['elo'] < opponent['elo'] and fight['result'] == 'Loss':
            self.log_positive_answer()
        elif fighter['elo'] >= opponent['elo'] and fight['result'] == 'Win':
            self.log_positive_answer()
        else:
            self.log_negative_answer()
    
    def pretty_print(self):
        with open("stats.txt", "w") as f:
            pretty_text = ""
            pretty_text += "CORRECT PREDICTIONS: " + str(self.correct_predictions) + "\n"
            pretty_text += "TOTAL PREDICTIONS: " + str(self.total_predictions) + "\n"
            if self.total_predictions > 0:
                pretty_text += "RATIO: " + str(self.correct_predictions / self.total_predictions) + "\n"
            f.write(pretty_text)
            f.close()