import discord
import asyncio
from discord.ext import commands

class Admin(commands.Cog):
    """Admin information commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong!")

def setup(bot):
    bot.add_cog(Admin(bot))