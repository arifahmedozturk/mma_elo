from DB.PSQLClient import PSQLClient

class EloChange(PSQLClient):
    def add_elo_change(self, fighter, opponent, opponent_elo, date, elo, new_elo):
        self.cursor.execute(
            "INSERT INTO elo_changes(fighter, opponent, opponent_elo, date, elo, new_elo) VALUES (%s, %s, %s, %s, %s, %s)",
            (fighter, opponent, opponent_elo, date, elo, new_elo)
        )
        self.connection.commit()

    def reset_table(self):
        self.cursor.execute("TRUNCATE TABLE elo_changes")
        self.connection.commit()
