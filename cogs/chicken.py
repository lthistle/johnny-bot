import discord
import time
import random
import asyncio
from discord.ext import commands

chicken_embed = discord.Embed(
    color = int("8f0bbf", 16),
    title = "Chicken Fighting",
)


class Chicken(commands.Cog):
    """Chicken fight ring commands"""
    def __init__(self, bot):
        self.bot = bot

    async def add_user(self, uid):
        """Adds a user to the database if they do not already exist"""
        await self.bot.db.execute(f"INSERT OR IGNORE INTO chickens (user_id, points, chicken_winrate) \
                                    VALUES ({uid}, 0, 0)")

    @commands.Cog.listener()
    async def on_message(self, message):
        uid = message.author.id
        await self.add_user(uid)
        #update points by 1 for each message
        await self.bot.db.execute(f"UPDATE chickens SET points = points + 1 WHERE user_id = {uid}")

    @commands.group()
    async def chicken(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid subcommand") #TODO: help menu instead of crappy message
    
    async def get_user_data(self, uid):
        await self.add_user(uid)
        rows = await self.bot.db.execute(f"SELECT points, chicken_winrate FROM chickens WHERE user_id = {uid}")
        return rows[0]

    @chicken.command()
    async def points(self, ctx):
        uid = ctx.author.id
        points = (await self.get_user_data(uid))[0]
        #format response
        response = chicken_embed.copy()
        response.description = f"<@{uid}> has {points} points."
        await ctx.send(embed=response)

    @chicken.command()
    async def buy(self, ctx):
        uid = ctx.author.id
        points, cwr = await self.get_user_data(uid)
        response = chicken_embed.copy()
        if cwr != 0:
            response.description = f"<@{uid}> you already own a chicken!"
        elif points < 10:
            response.description = f"<@{uid}> you only have {points} points. A chicken costs 10 points."
        else:
            await self.bot.db.execute(f"UPDATE chickens SET points = points - 10, chicken_winrate = 50 \
                                        WHERE user_id = {uid}")
            response.description = f"<@{uid}> you have purchased a chicken. {points - 10} points remaining."
        await ctx.send(embed=response)

    @chicken.command()
    async def bet(self, ctx, value : int):
        uid = ctx.author.id 
        points, cwr = await self.get_user_data(uid)
        response = chicken_embed.copy()
        good_bet = False
        if cwr == 0:
            response.description = f"<@{uid}> you do not own a chicken. Use ?chicken buy"
        elif value < 0:
            response.description = f"<@{uid}> stop trying to cheat."
        elif value > points:
            response.description = f"<@{uid}> you do not have enough points to make that bet."
        else:
            response.description = f"<@{uid}> you have entered your chicken into the fight ring with a {cwr}% \
                                     chance of winning."
            response.add_field(name="Results", value="Fight begins in 3...")
            good_bet = True
        msg = await ctx.send(embed=response)
        if good_bet:
            await asyncio.sleep(1)
            for x in [2, 1]:
                response.set_field_at(index=0, name="Results", value=f"Fight begins in {x}...")
                await msg.edit(embed=response)
                await asyncio.sleep(1)
            rng = random.randint(1, 100)
            if cwr >= rng: #fight won
                print("fight won")
                response.color = int("09de14", 16)
                response.set_field_at(index=0, name="Results: Fight Won!",
                                      value=f"You won **{value} points** and your chicken now has a **{cwr+1}% chance** to win future fights.")
                await self.bot.db.execute(f"UPDATE chickens SET points = points + {value}, chicken_winrate = chicken_winrate + 1 \
                                            WHERE user_id = {uid}")
                await msg.edit(embed=response)
            else: #fight lost
                print("fight lost")
                response.color = int("d60f09", 16)
                response.set_field_at(index=0, name="Results: Fight Lost!",
                                      value=f"You lost **{value} points** and your chicken died.")
                await self.bot.db.execute(f"UPDATE chickens SET points = points - {value}, chicken_winrate = 0 \
                                            WHERE user_id = {uid}")
                await msg.edit(embed=response)

    @bet.error
    async def bet_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
            response = chicken_embed.copy()
            response.description = "Invalid argument passed to 'bet' command. Example: ?chicken bet 100"
            await ctx.send(embed=response)
    
    @chicken.command()
    async def gift(self, ctx, value : int, **kwargs):
        people_mentioned = ctx.message.mentions
        if str(ctx.author) != "lthistle#5451":
            return
        #gift points to everyone mentioned
        for user in people_mentioned:
            uid = user.id
            await self.bot.db.execute(f"UPDATE chickens SET points = points + {value} WHERE user_id = {uid}")
        response = chicken_embed.copy()
        response.description = f"Gave {value} points to the following users: {', '.join([str(user) for user in people_mentioned])}"
        await ctx.send(embed=response)
        #if ctx.author.name == "lthistle#5451":

def setup(bot):
    bot.add_cog(Chicken(bot))