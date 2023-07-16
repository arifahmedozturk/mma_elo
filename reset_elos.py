from DB.EloChange import EloChange
from DB.Fighter import Fighter

eloChangeDB = EloChange()
eloChangeDB.reset_table()

fighterDB = Fighter()
fighterDB.reset_fighters_elo()
fighterDB.reset_fighters_last_age_penalty()

with open("last_date.txt", "w") as f:
    f.write('"1940-01-01"')