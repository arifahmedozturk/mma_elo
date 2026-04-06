from DB.PSQLClient import PSQLClient

class Fighter(PSQLClient):
    def add_fighter(self, fighter_name, dob):
        if dob is not None:
            self.cursor.execute(
                "INSERT INTO fighters(fighter_name, elo, dob, last_age_penalty) VALUES (%s, %s, %s, %s)",
                (fighter_name, self.config.STARTING_ELO, dob, self.date_helper.add_years_to_date(dob, self.config.MIN_AGE_FOR_PENALTY))
            )
        else:
            self.cursor.execute(
                "INSERT INTO fighters(fighter_name, elo) VALUES (%s, %s)",
                (fighter_name, self.config.STARTING_ELO)
            )
        self.connection.commit()

    def get_fighter(self, fighter_name, add_if_not_present=True):
        self.cursor.execute(
            "SELECT fighter_name, elo, dob, last_age_penalty FROM fighters WHERE fighter_name=%s",
            (fighter_name,)
        )
        fighters = self.cursor.fetchall()
        if len(fighters) == 0:
            if not add_if_not_present:
                return None

            self.add_fighter(fighter_name, None)
            fighters = [[fighter_name, self.config.STARTING_ELO, None, None]]

        return {
            'name': fighters[0][0],
            'elo': fighters[0][1],
            'dob': fighters[0][2],
            'last_age_penalty': fighters[0][3]
        }

    def get_fighters(self):
        self.cursor.execute("SELECT fighter_name, elo, dob, last_age_penalty FROM fighters;")
        fighters = self.cursor.fetchall()
        return [
            {
                'name': f[0],
                'elo': f[1],
                'dob': f[2],
                'last_age_penalty': f[3]
            }
            for f in fighters
        ]

    def reset_fighters_elo(self):
        self.cursor.execute("UPDATE fighters SET elo=%s", (self.config.STARTING_ELO,))
        self.connection.commit()

    def set_fighter_elo(self, fighter_name, elo):
        self.cursor.execute(
            "UPDATE fighters SET elo=%s WHERE fighter_name=%s",
            (elo, fighter_name)
        )
        self.connection.commit()

    def reset_fighters_last_age_penalty(self):
        fighters = self.get_fighters()
        for fighter in fighters:
            if fighter['dob'] is None:
                continue
            self.cursor.execute(
                "UPDATE fighters SET last_age_penalty=%s WHERE fighter_name=%s",
                (self.date_helper.add_years_to_date(fighter['dob'], self.config.MIN_AGE_FOR_PENALTY), fighter['name'])
            )
            self.connection.commit()

    def set_fighter_last_age_penalty(self, fighter_name, last_age_penalty):
        if last_age_penalty is None:
            return
        self.cursor.execute(
            "UPDATE fighters SET last_age_penalty=%s WHERE fighter_name=%s",
            (last_age_penalty, fighter_name)
        )
        self.connection.commit()
