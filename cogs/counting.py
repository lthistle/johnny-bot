import ast
import discord
import time
import random
import asyncio
import operator as op
import simpleeval
import ctypes

import simpleeval
from discord.ext import commands

counting_embed = discord.Embed(
    color = int("d1b0fc", 16),
    title = "Pro counting",
)

failure_counting_embed = discord.Embed(
    color = int("fc8890", 16),
    title = "Pro counting",
)


def bitwise_not_unsigned(x):
    bit_num = len(bin(x))

    print("bit num is " + str(bit_num))

    if bit_num >= 64:
        return ctypes.c_uint64(~x).value
    if bit_num >= 32:
        return ctypes.c_uint32(~x).value
    elif bit_num >= 16:
        return ctypes.c_uint16(~x).value
    else:
        return ctypes.c_uint8(~x).value


custom_operators = [(ast.BitXor, simpleeval.safe_power),
                    (ast.Invert, bitwise_not_unsigned),
                    (ast.BitOr, lambda x, y: x | y),
                    (ast.BitAnd, lambda x, y: x & y),
                    (ast.LShift, lambda x, y: x << y),
                    (ast.RShift, lambda x, y: x >> y)]


class Counting(commands.Cog):
    """Better counting commands"""

    def __init__(self, bot):
        self.bot = bot
        self.simple_eval = simpleeval.SimpleEval()

        for custom_operator in custom_operators:
            self.simple_eval.operators[custom_operator[0]] = custom_operator[1]

    @commands.group()
    async def counting(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.message.reply("Invalid subcommand")

    @commands.Cog.listener()
    async def on_message(self, message):
        # TODO: There has to be a better way to check the validity of a message than this...
        if len(message.content) <= 0:
            return
        elif message.content[0].isdigit() or (message.content[0] == '~' and \
                message.content[1].isdigit()) or (message.content[0] == '(' and message.content[1].isdigit()):
            expected_value = await self.bot.db.execute(f"SELECT current_number FROM counter_table WHERE "
                                                       f"channel_id={message.channel.id} AND guild_id={message.guild.id}")

            if expected_value is None or len(expected_value) <= 0:
                return
            else:
                expected_value = expected_value[0][0]

            print(expected_value)

            user_value = self.simple_eval.eval(message.content)

            if expected_value == user_value:
                new_value = expected_value + 1

                await message.add_reaction("✅")
            else:
                new_value = 1

                await message.add_reaction("❌")

                response = failure_counting_embed.copy()
                response.description = f"YOU RUINED IT at {expected_value}! You instead said {user_value}! START AT ONE AGAIN!!!"

                await message.reply(embed=response)

            await self.bot.db.execute(f"UPDATE counter_table SET current_number = {new_value}")

    @counting.command()
    async def setchannel(self, ctx):
        guild_result = ctx.message.guild

        if guild_result is None:
            response = failure_counting_embed.copy()
            response.description = "This command must be executed in a server!"

            await ctx.message.reply(embed=response)
        elif not ctx.message.author.guild_permissions.administrator and ctx.message.author.id != 192011183367258113:
            response = failure_counting_embed.copy()
            response.description = "You must be an admin or a very cool person to execute this command!"

            await ctx.message.reply(embed=response)
        elif len(ctx.message.channel_mentions) <= 0:
            response = failure_counting_embed.copy()
            response.description = "Please mention a channel to be marked as the counting channel!"

            await ctx.message.reply(embed=response)
        else:
            await self.bot.db.execute(f"DELETE FROM counter_table WHERE guild_id={guild_result.id}")

            await self.bot.db.execute(f"INSERT INTO counter_table (guild_id, channel_id, current_number) VALUES "
                                      f"({guild_result.id}, {ctx.message.channel_mentions[0].id}, {1})")

            response = counting_embed.copy()
            response.description = f"Counting channel successfully set to #{ctx.message.channel_mentions[0].name}"

            await ctx.message.reply(embed=response)

    @counting.command()
    async def serverstats(self, ctx):
        guild_result = ctx.message.guild

        if guild_result is None:
            response = failure_counting_embed.copy()
            response.description = "This command must be executed in a server!"

            await ctx.message.reply(embed=response)
        else:
            guild_row = await self.bot.db.execute(f"SELECT FROM counter_table WHERE guild_id={guild_result.id}")

            if guild_row is None or len(guild_row) <= 0:
                response = failure_counting_embed.copy()
                response.description = "No server stats are available yet! Try creating a counting channel"

                await ctx.message.reply(embed=response)
            else:
                target_user = ctx.message.author

                if len(ctx.message.mentions) > 0:
                    target_user = ctx.message.mentions[0]

                response = counting_embed.copy()
                response.set_image(target_user.avatar_url)

                user_stats = await self.bot.db.execute(f"SELECT ")

    @counting.command()
    async def userstats(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Counting(bot))