import ast
import discord
import time
import random
import asyncio
import operator as op
import simpleeval
import ctypes

import simpleeval
from datetime import datetime
from discord.ext import commands

counting_embed = discord.Embed(
    color = int("d1b0fc", 16),
    title = "Pro counting",
)

failure_counting_embed = discord.Embed(
    color = int("fc8890", 16),
    title = "Pro counting",
)

new_record_embed = discord.Embed(
    color = int("fceb6c", 16),
    title = "🏆 NEW SERVER RECORD!!!",
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
        self.record_reached = False

        for custom_operator in custom_operators:
            self.simple_eval.operators[custom_operator[0]] = custom_operator[1]

    def _get_human_readable_time(self, timestamp: int) -> str:
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

    @commands.group()
    async def counting(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.message.reply("Invalid subcommand")

    @commands.Cog.listener()
    async def on_message(self, message):
        # TODO: There has to be a better way to check the validity of a message than this...
        if len(message.content) <= 0:
            return
        elif message.content[0].isdigit() or (message.content[0] == '~' and
                message.content[1].isdigit()) or (message.content[0] == '(' and message.content[1].isdigit()):
            guild_stats = await self.bot.db.execute(f"SELECT current_number, highest_number, highest_number_timestamp, "
                                                   f"last_count, last_count_timestamp, longest_counting_delay_sec "
                                                   f"FROM counter_table WHERE channel_id={message.channel.id} "
                                                   f"AND guild_id={message.guild.id}")
            user_stats = await self.bot.db.execute(f"SELECT * FROM counter_leaderboard WHERE "
                                                   f"user_id={message.author.id}")

            if guild_stats is None or len(guild_stats) <= 0:
                return
            else:
                guild_stats = guild_stats[0]

                expected_value = guild_stats[0]

                if user_stats is None or len(user_stats) <= 0:
                    user_stats = [message.author.id, 0, 0, 0, 0, 0]

                    await self.bot.db.execute(f"INSERT INTO")


            print(expected_value)

            user_value = self.simple_eval.eval(message.content)

            if expected_value == user_value:
                new_value = expected_value + 1

                # guild stat code
                if expected_value > guild_stats[1]:
                    if not self.record_reached:
                        response = new_record_embed.copy()

                        response.timestamp = message.created_at
                        response.description = f"Reached {expected_value}!"

                        await message.reply(embed=response)

                        self.record_reached = True

                    guild_stats[1] = expected_value
                    guild_stats[2] = message.created_at

                if message.created_at - guild_stats[4] > guild_stats[5]:
                    guild_stats[5] = message.created_at - guild_stats[4]

                guild_stats[3] = expected_value
                guild_stats[4] = message.created_at

                # user stat code
                if expected_value > user_stats[1]:
                    user_stats[1] = expected_value
                    user_stats[2] = message.created_at

                user_stats[3] += 1

                await message.add_reaction("✅")
            else:
                new_value = 1

                self.record_reached = False

                user_stats[4] += 1

                if expected_value > user_stats[4]:
                    user_stats[5] = expected_value
                    user_stats[6] = message.created_at

                await message.add_reaction("❌")

                response = failure_counting_embed.copy()
                response.description = f"YOU RUINED IT at {expected_value}! You instead said {user_value}! START AT ONE AGAIN!!!"

                await message.reply(embed=response)

            await self.bot.db.execute(f"UPDATE counter_table SET current_number = {new_value}, "
                                      f"highest_number = {guild_stats[1]}, highest_number_timestamp = {guild_stats[2]}"
                                      f"last_count = {guild_stats[3]}, last_count_timestamp = {guild_stats[4]}, "
                                      f"longest_counting_delay_sec = {guild_stats[5]} WHERE "
                                      f"channel_id={message.channel.id} AND guild_id={message.guild.id}")
            await self.bot.db.execute(f"UPDATE counter_leaderboard SET highest_number = {user_stats[1]}, "
                                      f"highest_number_timestamp = {user_stats[2]}, successful_counts = {user_stats[3]},"
                                      f"failed_counts = {user_stats[4]}, worst_miscount_num = {user_stats[5]}, "
                                      f"worst_miscount_timestamp = {user_stats[6]} WHERE user_id={message.author.id}")

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

            await self.bot.db.execute(f"INSERT INTO counter_table (guild_id, channel_id, current_number, highest_number,"
                                      f"highest_number_timestamp, last_count, last_count_timestamp, "
                                      f"longest_counting_delay_sec) VALUES ({guild_result.id}, "
                                      f"{ctx.message.channel_mentions[0].id}, {1}, {0}, {0}, {0}, {0}, {0})")

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
            guild_row = await self.bot.db.execute(f"SELECT * FROM counter_table WHERE guild_id={guild_result.id}")

            if guild_row is None or len(guild_row) <= 0:
                response = failure_counting_embed.copy()
                response.description = "No server stats are available yet! Try creating a counting channel"

                await ctx.message.reply(embed=response)
            else:
                guild_row = guild_row[0]

                response = counting_embed.copy()
                response.title += "- Server-wide stats"

                response.set_image(ctx.message.guild.icon_url)

                response.add_field("Highest number counted to", f"{guild_row[3]} at "
                                                                f"{self._get_human_readable_time(guild_row[4])}")
                response.add_field("Last count", f"To {guild_row[5]} at {self._get_human_readable_time(guild_row[6])}")
                response.add_field("Longest time between counting", f"{guild_row[7]} seconds")

                await ctx.message.reply(embed=response)

    @counting.command()
    async def userstats(self, ctx):
        target_user = ctx.message.author

        if len(ctx.message.mentions) > 0:
            target_user = ctx.message.mentions[0]

        user_stats = await self.bot.db.execute(f"SELECT * FROM counter_leaderboard WHERE "
                                               f"user_id={target_user.id}")

        if user_stats is None or len(user_stats) <= 0:
            response = failure_counting_embed.copy()
            response.description = "No stats from this user are available yet!"

            await ctx.message.reply(embed=response)
        else:
            user_stats = user_stats[0]

            response = counting_embed.copy()
            response.title += f"{target_user.display_name}'s stats"

            response.set_image(target_user.avatar_url)

            response.add_field("Highest number counted to", f"{user_stats[1]}")
            response.add_field("Successful counts", f"{user_stats[2]}")
            response.add_field("Unsuccessful counts", f"{user_stats[3]}")
            response.add_field("Accuracy", f"{(float(user_stats[2]) / (user_stats[2] + user_stats[3]) * 100)}%")
            response.add_field("Worst miscount", f"Didn't count to {user_stats[4]} at {user_stats[5]}")

            await ctx.message.reply(embed=response)



def setup(bot):
    bot.add_cog(Counting(bot))