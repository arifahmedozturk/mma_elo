from DB.PSQLClient import PSQLClient

class EloChange(PSQLClient):
    def add_elo_change(self, fighter, opponent, opponent_elo, date, elo, new_elo):
        psql_script = "INSERT INTO elo_changes(fighter, opponent, opponent_elo, date, elo, new_elo) VALUES ('" + fighter.replace("'", "''") + "', '" + opponent.replace("'", "''") + "', " + str(opponent_elo) + ", '" + date + "', " + str(elo) + ", " + str(new_elo) + ");"
        self.cursor.execute(psql_script)
        self.connection.commit()

    def reset_table(self):
        self.cursor.execute("TRUNCATE TABLE elo_changes")
        self.connection.commit()