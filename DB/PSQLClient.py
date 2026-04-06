import psycopg2
import os
from Config.Config import Config
from Helpers.DateHelper import DateHelper

class PSQLClient:
    def __init__(self):
        self.connection, self.cursor = self.setup_connection()
        self.config = Config()
        self.date_helper = DateHelper()

    def setup_connection(self):
        connection = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            user=os.getenv('DB_USER', 'myuser'),
            password=os.getenv('DB_PASSWORD', 'mypassword'),
            database=os.getenv('DB_NAME', 'mydatabase')
        )

        cursor = connection.cursor()
        return connection, cursor