from DB.PSQLClient import PSQLClient

class Fight(PSQLClient):
    def add_fight(self, fighter, opponent, result, date, method, event):
        self.cursor.execute(
            "INSERT INTO fights(fighter, opponent, result, date, method, event) VALUES (%s, %s, %s, %s, %s, %s)",
            (fighter, opponent, result, date, method, event)
        )
        self.connection.commit()

    def serialize_fights(self, fights):
        return [
            {
                'fighter': f[0],
                'opponent': f[1],
                'result': f[2],
                'date': f[3],
                'method': f[4],
                'event': f[5]
            }
            for f in fights
        ]

    def get_fights(self):
        self.cursor.execute("SELECT fighter, opponent, result, date, method, event FROM fights;")
        return self.serialize_fights(self.cursor.fetchall())

    def get_fights_at_date(self, date):
        self.cursor.execute(
            "SELECT fighter, opponent, result, date, method, event FROM fights WHERE date=%s",
            (date,)
        )
        return self.serialize_fights(self.cursor.fetchall())

    def get_closest_date_to_date(self, date):
        self.cursor.execute(
            "SELECT date FROM fights WHERE %s < date ORDER BY date LIMIT 1",
            (date,)
        )
        dates = self.cursor.fetchall()
        if len(dates) == 0:
            return None

        return dates[0][0]
