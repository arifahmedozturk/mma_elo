from DB import Fight, Fighter

FighterDB = Fighter.Fighter()
fighters = FighterDB.get_fighters()
fighter_insert_text = ""
for fighter in fighters:
    psql_script = "INSERT INTO fighters(fighter_name, elo) VALUES ('" + fighter['name'].replace("'", "''") + "', " + str(fighter['elo']) + ");"
    if fighter['dob'] is not None:
        psql_script = "INSERT INTO fighters(fighter_name, elo, dob, last_age_penalty) VALUES ('" + fighter['name'].replace("'", "''") + "', " + str(fighter['elo']) + ", '" + fighter['dob'] + "', '" + fighter['last_age_penalty'] + "');"
    fighter_insert_text += psql_script + "\n"
with open("fighters.sql", "w", encoding="utf-8") as f:
    f.write(fighter_insert_text)
    f.close()

FightDB = Fight.Fight()
fights = FightDB.get_fights()
fight_insert_text = ""
for fight in fights:
    fight_insert_text += "INSERT INTO fights(fighter, opponent, result, date, method, event) VALUES ('" + fight['fighter'].replace("'", "''") + "', '" + fight['opponent'].replace("'", "''") + "', '" + fight['result'].replace("'", "''") + "', '" + fight['date'] + "', '" + fight['method'].replace("'", "''") + "', '" + fight['event'].replace("'", "''") + "');"
    fight_insert_text += "\n"
with open("fights.sql", "w", encoding="utf-8") as f:
    f.write(fight_insert_text)
    f.close()