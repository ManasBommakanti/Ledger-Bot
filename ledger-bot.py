import discord
from discord.ext import commands
from discord.commands import Option

import json
import asyncio

description = """
    Bot to store poker ledgers for poker game nights.
"""

secrets = json.load(open("secrets/secrets.json"))

intents = discord.Intents.all()
intents.members = True
intents.message_content = True

bot = discord.Bot()
ledger = discord.SlashCommandGroup("ledger", "ledger command group")
client = discord.Client()

"""
HELPER FUNCTIONS
"""


# Gets the username of Discord Member
async def get_username(ctx, member: discord.Member) -> str:
    if member is None:
        # If no member is specified, use the author's username
        name = ctx.author.display_name
    else:
        # Use the specified member's username
        name = member.display_name

    print("USERNAME: ", name)

    return name


# Gets the latest data from Ledger System
async def get_data(ctx) -> dict:
    # Load existing data from the ledger.json file
    try:
        with open("secrets/ledger.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist, initialize data as an empty dictionary
        data = {}
        print("Cannot find secrets/ledger.json")
    except Exception as e:
        print(e)
        embed = discord.Embed(
            title="Error!",
            description=f"Something is wrong internally :(",
            color=discord.Colour.red(),
        )
        return await ctx.respond(embed=embed)

    return data


# Update data of Ledger System
async def update_data(ctx, data: dict):
    # Save the updated data back to the ledger.json file
    try:
        with open("secrets/ledger.json", "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(e)
        embed = discord.Embed(
            title="Error!",
            description=f"Something is wrong internally :(",
            color=discord.Colour.red(),
        )
        return await ctx.respond(embed=embed)


"""
COMMAND FUNCTIONS
"""


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


@ledger.command(
    name="addplayer", description="Add yourself or another user to the Poker Ledger"
)
async def addplayer(ctx, member: discord.Member = None):
    name = await get_username(ctx, member)
    data = await get_data(ctx)

    # Check if the player with the given name already exists
    if name in data:
        embed = discord.Embed(
            title="Error!",
            description=f"Player with username **{name}** already exists.",
            color=discord.Colour.dark_red(),
        )
        return await ctx.respond(embed=embed)

    # Add the new player to the data
    data[name] = {
        "name": name,
        "bank": 800,
        "hands_won": 0,
        "hands_lost": 0,
        "folds": 0,
    }

    await update_data(ctx, data)

    embed = discord.Embed(
        title="Player Added!",
        description=f"Welcome **{name}**!",
        color=discord.Colour.dark_green(),
    )

    await ctx.respond(embed=embed)


@ledger.command(name="stats", description="Get your or another player's Poker stats")
async def stats(ctx, member: discord.Member = None):
    name = await get_username(ctx, member)
    data = await get_data(ctx)

    # Check if the player with the given name does not exist
    if name not in data:
        embed = discord.Embed(
            title="Error!",
            description=f"Player with username **{name}** is not in Ledger System.",
            color=discord.Colour.dark_red(),
        )
        return await ctx.respond(embed=embed)

    user_stats = data[name]
    stats_message = (
        f"Player **{name}**\n\n"
        f"Bank: ${user_stats['bank']}\n"
        f"Hands Won: {user_stats['hands_won']}\n"
        f"Hands Lost: {user_stats['hands_lost']}\n"
        f"Folds: {user_stats['folds']}\n"
    )

    embed = discord.Embed(
        title="Statistics",
        description=stats_message,
        colour=discord.Colour.blue(),
    )

    await ctx.respond(embed=embed)


@ledger.command(name="addwin", description="Add a win to yourself or another player")
async def addwin(ctx, member: discord.Member = None):
    name = get_username(ctx, member)
    data = get_data(ctx)

    # Check if the player with the given name already exists
    if name not in data:
        embed = discord.Embed(
            title="Error!",
            description=f"Player with username **{name}** is not in Ledger System.",
            color=discord.Colour.dark_red(),
        )
        return await ctx.respond(embed=embed)

    update_wins = data[name]["hands_won"] + 1
    data[name]["hands_won"] = update_wins

    update_data(ctx, data)

    embed = discord.Embed(
        title=f"Updating Win",
        description=(
            f"*Added* one win to Player {name}!\n" f"Total Wins: {update_wins}\n"
        ),
        colour=discord.Colour.green(),
    )

    await ctx.respond(embed=embed)


@ledger.command(
    name="removewin", description="Remove a win from yourself or another player"
)
async def removewin(ctx, member: discord.Member):
    name = get_username(ctx, member)
    data = get_data(ctx)

    # Check if the player with the given name already exists
    if name not in data:
        embed = discord.Embed(
            title="Error!",
            description=f"Player with username **{name}** is not in Ledger System.",
            color=discord.Colour.dark_red(),
        )
        return await ctx.respond(embed=embed)

    # Check if hands_won = 0 because we cannot go negative
    if data[name]["hands_won"] <= 0:
        embed = discord.Embed(
            title="Error!",
            description=f"Player {name} did not win anything :(\n"
            f"Cannot remove from 0 wins",
            color=discord.Colour.dark_red(),
        )
        return await ctx.respond(embed=embed)

    update_wins = data[name]["hands_won"] - 1
    data[name]["hands_won"] = update_wins

    update_data(ctx, data)

    embed = discord.Embed(
        title=f"Updating Win",
        description=(
            f"*Removed* one win to Player {name}!\n" f"Total Wins: {update_wins}\n"
        ),
        colour=discord.Colour.red(),
    )

    await ctx.respond(embed=embed)


@ledger.command()
async def addloss(ctx, member: discord.Member):
    # Load existing data from the ledger.json file
    try:
        with open("secrets/ledger.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist, initialize data as an empty dictionary
        data = {}

    # Check if the player with the given name already exists
    if name not in data:
        return await ctx.respond(f"Player {name} does not exist!")

    update_loss = data[name]["hands_lost"] + 1
    data[name]["hands_lost"] = update_loss

    # Save the updated data back to the ledger.json file
    with open("secrets/ledger.json", "w") as f:
        json.dump(data, f, indent=4)

    message = f"Added one win to Player {name}\n" f"Total Wins: {update_loss}\n"

    await ctx.respond(message)


@ledger.command()
async def removeloss(ctx, name: str):
    # Load existing data from the ledger.json file
    try:
        with open("secrets/ledger.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist, initialize data as an empty dictionary
        data = {}

    # Check if the player with the given name already exists
    if name not in data:
        return await ctx.respond(f"Player {name} does not exist!")

    # Check if player has more than 0 losses in order to remove one
    if data[name]["hands_lost"] == 0:
        return await ctx.respond(f"Player {name} has 0 losses. Cannot remove loss!")

    # Check if hands_lost = 0 because we cannot go negative
    if data[name]["hands_lost"] <= 0:
        return await ctx.respond(
            (
                f"Player {name} did not lose anything... yet\n"
                f"Cannot remove from 0 losses"
            )
        )

    update_loss = data[name]["hands_lost"] - 1
    data[name]["hands_lost"] = update_loss

    # Save the updated data back to the ledger.json file
    with open("secrets/ledger.json", "w") as f:
        json.dump(data, f, indent=4)

    message = f"Removed one win to Player {name}\n" f"Total Wins: {update_loss}\n"

    await ctx.respond(message)


@ledger.command()
async def addfold(ctx, name: str):
    # Load existing data from the ledger.json file
    try:
        with open("secrets/ledger.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist, initialize data as an empty dictionary
        data = {}

    # Check if the player with the given name already exists
    if name not in data:
        return await ctx.respond(f"Player {name} does not exist!")

    update_folds = data[name]["folds"] + 1
    data[name]["folds"] = update_folds

    # Save the updated data back to the ledger.json file
    with open("secrets/ledger.json", "w") as f:
        json.dump(data, f, indent=4)

    message = f"Added one win to Player {name}\n" f"Total Wins: {update_folds}\n"

    await ctx.respond(message)


@ledger.command()
async def removefold(ctx, name: str):
    # Load existing data from the ledger.json file
    try:
        with open("secrets/ledger.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist, initialize data as an empty dictionary
        data = {}

    # Check if the player with the given name already exists
    if name not in data:
        return await ctx.respond(f"Player {name} does not exist!")

    # Check if folds = 0 because we cannot go negative
    if data[name]["folds"] <= 0:
        return await ctx.respond(
            (
                f"Player {name} did not fold anytime (idk how)\n"
                f"Cannot remove from 0 folds"
            )
        )

    update_fold = data[name]["folds"] - 1
    data[name]["hands_won"] = update_fold

    # Save the updated data back to the ledger.json file
    with open("secrets/ledger.json", "w") as f:
        json.dump(data, f, indent=4)

    message = f"Removed one win to Player {name}\n" f"Total Wins: {update_fold}\n"

    await ctx.respond(message)


bot.add_application_command(ledger)
bot.run(secrets["TOKEN"])
