import discord
import os, sys
import time
import sqlite3
from modules import database
from discord.ext import commands

#@TODO: Make real config settings
TOKEN = os.environ["JBOT_DISCORD_TOKEN"]
prefix = "?"
class JohnnyBot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.default_prefix = prefix
        self.start_time = time.time()
        self.db = database.SqliteDB(self)

bot = JohnnyBot(
    command_prefix = prefix,
)

extensions = [
    "chicken"
]

if __name__ == "__main__":
    #inspired by miso bot
    for extension in extensions:
        #try:
        bot.load_extension(f"cogs.{extension}")
        #except Exception as error:
        #    print(f"Could not load extension {extension}")
    bot.run(TOKEN)




#?chicken buy
#?chicken points
#?chicken bet
#admin commands: uptime, shutdown