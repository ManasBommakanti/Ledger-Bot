import discord
from discord.ext import commands

import json

secrets = json.load(open("secrets.json"))

description = """
    Bot to store poker ledgers for poker game nights.
"""

intents = discord.Intents.all()
intents.members = True
intents.message_content = True

# bot = commands.Bot(description=description, intents=intents)
bot = discord.Bot()
math = discord.SlashCommandGroup("math", "Math related commands")


@bot.command(
    description="Sends the bot's latency."
)  # this decorator makes a slash command
async def ping(ctx):  # a slash command will be created with the name "ping"
    await ctx.respond(f"Pong! Latency is {bot.latency}")


@math.command()
async def add(ctx, num1: int, num2: int):
    sum = num1 + num2
    await ctx.respond(f"{num1} plus {num2} is {sum}.")


@math.command()
async def subtract(ctx, num1: int, num2: int):
    sum = num1 - num2
    await ctx.respond(f"{num1} minus {num2} is {sum}.")


# you'll have to manually add the manually created Slash Command group
bot.add_application_command(math)
bot.run(secrets["TOKEN"])
