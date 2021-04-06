import discord
import asyncio
from discord.ext import commands

class Admin(commands.Cog):
    """Admin information commands"""
    def __init__(self, bot):
        self.bot = bot
    
    