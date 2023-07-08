from DB.PSQLClient import PSQLClient

class Fight(PSQLClient):
    def add_fight(self, fighter, opponent, result, date, method, event):
        self.cursor.execute("INSERT INTO fights(fighter, opponent, result, date, method, event) VALUES ('" + fighter.replace("'", "''") + "', '" + opponent.replace("'", "''") + "', '" + result.replace("'", "''") + "', '" + date + "', '" + method.replace("'", "''") + "', '" + event.replace("'", "''") + "');")
        self.connection.commit()
    
    def serialize_fights(self, fights):
        fight_dicts = []
        for fight in fights:
            fight_dicts.append({
                'fighter': fight[0],
                'opponent': fight[1],
                'result': fight[2],
                'date': fight[3],
                'method': fight[4],
                'event': fight[5]
            })
        
        return fight_dicts
    
    def get_fights(self):
        self.cursor.execute("SELECT fighter, opponent, result, date, method, event FROM fights;")
        fights = self.cursor.fetchall()
        return self.serialize_fights(fights)

    def get_fights_at_date(self, date):
        self.cursor.execute("SELECT fighter, opponent, result, date, method, event FROM fights WHERE date='" + date + "';")
        fights = self.cursor.fetchall()
        return self.serialize_fights(fights)
    
    def get_closest_date_to_date(self, date):
        self.cursor.execute("SELECT date FROM fights WHERE '" + date + "' < date ORDER BY date LIMIT 1;")
        dates = self.cursor.fetchall()
        if len(dates) == 0:
            return None
        
        return dates[0][0]