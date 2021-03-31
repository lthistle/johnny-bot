import sqlite3
import asyncio
db_file = "data/database.db"

class SqliteDB:
    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.init_connection())

    async def init_connection(self):
        conn = None
        try: 
            conn = sqlite3.connect(db_file)
            print("Sucessfully connected to database.")
        except Error as e:
            print(e)
        self.conn = conn

    async def execute(self, statement):
        try:
            c = self.conn.cursor()
            c.execute(statement)
            self.conn.commit()
            rows = c.fetchall()
            return rows
        except Error as e:
            print(e)