from DB.Fighter import Fighter

fighterDB = Fighter()
fighterDB.reset_fighters_elo()
fighterDB.reset_fighters_last_age_penalty()

with open("last_date.txt", "w") as f:
    f.write('"1940-01-01"')