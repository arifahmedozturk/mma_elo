import psycopg2
from Config.Config import Config
from Helpers.DateHelper import DateHelper

class PSQLClient:
    def __init__(self):
        self.connection, self.cursor = self.setup_connection()
        self.config = Config()
        self.date_helper = DateHelper()

    def setup_connection(self):
        connection = psycopg2.connect(
            host='localhost',
            port='5432', 
            user='myuser', 
            password='mypassword',
            database='mydatabase'
        )

        cursor = connection.cursor()
        return connection, cursor