from DB.Fighter import Fighter

f = Fighter()

f.reset_fighters_elo()
f.reset_fighters_last_age_penalty()
with open("last_date.txt", "w"):
    f.write("1940-01-01")