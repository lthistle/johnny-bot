import discord
from discord.ext import commands
import PIL

class Alan(commands.Cog):
    """Set of commands to downscale then upscale images (inspired by Alan)"""
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def alan(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid subcommand")

    @alan.command()
    async def beautify(self, ctx):
        uid = ctx.author.id
        replied = ctx.message.reference
        if not replied:
            return
        msg = await ctx.fetch_message(replied.message_id)
        print(msg.embeds[0].url)
        #print(msg.)

    #msg.embeds.url has the image url
    #ctx.message.reference
    #?alan beautify 100 (fuckery factor)

def setup(bot):
    bot.add_cog(Alan(bot))