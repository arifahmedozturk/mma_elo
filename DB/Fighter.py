from DB.PSQLClient import PSQLClient

class Fighter(PSQLClient):
    def add_fighter(self, fighter_name, dob):
        psql_script = "INSERT INTO fighters(fighter_name, elo) VALUES ('" + fighter_name.replace("'", "''") + "'," + str(self.config.STARTING_ELO) + ")"
        if dob is not None:
            psql_script = "INSERT INTO fighters(fighter_name, elo, dob, last_age_penalty) VALUES ('" + fighter_name.replace("'", "''") + "', " + str(self.config.STARTING_ELO) + ", '" + dob + "', '" + dob + "')"
        self.cursor.execute(psql_script)
        self.connection.commit()
    
    def get_fighter(self, fighter_name):
        self.cursor.execute("SELECT fighter_name, elo, dob, last_age_penalty FROM fighters WHERE fighter_name='" + fighter_name.replace("'", "''") + "';")
        fighters = self.cursor.fetchall()
        if len(fighters) == 0:
            self.add_fighter(fighter_name, None)
            fighters = [[fighter_name, self.config.STARTING_ELO, None, None]]
        return {
            'name': fighters[0][0],
            'elo': fighters[0][1],
            'dob': fighters[0][2],
            'last_age_penalty': fighters[0][3]
        }

    def get_fighters(self):
        fighter_dicts = []
        self.cursor.execute("SELECT fighter_name, elo, dob, last_age_penalty FROM fighters;")
        fighters = self.cursor.fetchall()
        for i in range(len(fighters)):
            if(len(fighters[i]) < 4):
                print(fighters[i])
            fighter_dicts.append({
                'name': fighters[i][0],
                'elo': fighters[i][1],
                'dob': fighters[i][2],
                'last_age_penalty': fighters[i][3]
            })
        return fighter_dicts

    def set_fighter_elo(self, fighter_name, elo):
        self.cursor.execute("UPDATE fighters SET elo=" + str(elo) + " WHERE fighter_name='" + fighter_name.replace("'", "''") + "';")
        self.connection.commit() 

    def set_fighter_last_age_penalty(self, fighter_name, last_age_penalty):
        self.cursor.execute("UPDATE fighters SET last_age_penalty='" + last_age_penalty + "' WHERE fighter_name='" + fighter_name.replace("'", "''") + "';")
        self.connection.commit() 