import discord
from discord.ext import commands
import random

import json

description = """
    Bot to store poker ledgers for poker game nights.
"""

secrets = json.load(open("secrets/secrets.json"))

intents = discord.Intents.all()
intents.members = True
intents.message_content = True

bot = discord.Bot()
ledger = discord.SlashCommandGroup("ledger", "ledger command group")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


@ledger.command()
async def addplayer(ctx, name: str):
    # Load existing data from the ledger.json file
    try:
        with open("secrets/ledger.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist, initialize data as an empty dictionary
        data = {}

    # Check if the player with the given name already exists
    if name in data:
        return await ctx.send("User already exists!")

    # Add the new player to the data
    data[name] = {
        "name": name,
        "bank": 800,
        "hands_won": 0,
        "hands_lost": 0,
        "folds": 0,
    }

    # Save the updated data back to the ledger.json file
    with open("secrets/ledger.json", "w") as f:
        json.dump(data, f, indent=4)

    await ctx.send(f"Player {name} added successfully!")


@ledger.command()
async def showstats(ctx, name: str):
    # Load existing data from the ledger.json file
    try:
        with open("secrets/ledger.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist, initialize data as an empty dictionary
        data = {}

    # Check if the player with the given name already exists
    if name not in data:
        return await ctx.send(f"Player {name} does not exist!")

    user_stats = data[name]
    stats_message = (
        f"Stats for {name}:\n"
        f"Bank: {user_stats['bank']}\n"
        f"Hands Won: {user_stats['hands_won']}\n"
        f"Hands Lost: {user_stats['hands_lost']}\n"
        f"Folds: {user_stats['folds']}\n"
    )

    await ctx.send(stats_message)


@ledger.command()
async def addwin(ctx, name: str):
    # Load existing data from the ledger.json file
    try:
        with open("secrets/ledger.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist, initialize data as an empty dictionary
        data = {}

    # Check if the player with the given name already exists
    if name not in data:
        return await ctx.send(f"Player {name} does not exist!")

    update_wins = data[name]["hands_won"] + 1
    data[name]["hands_won"] = update_wins

    # Save the updated data back to the ledger.json file
    with open("secrets/ledger.json", "w") as f:
        json.dump(data, f, indent=4)

    message = f"Added one win to Player {name}\n" f"Total Wins: {update_wins}\n"

    await ctx.send(message)


@ledger.command()
async def removewin(ctx, name: str):
    # Load existing data from the ledger.json file
    try:
        with open("secrets/ledger.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist, initialize data as an empty dictionary
        data = {}

    # Check if the player with the given name already exists
    if name not in data:
        return await ctx.send(f"Player {name} does not exist!")

    # Check if hands_won = 0 because we cannot go negative
    if data[name]["hands_won"] <= 0:
        return await ctx.send(
            (f"Player {name} did not win anything :(\n" f"Cannot remove from 0 wins")
        )

    update_wins = data[name]["hands_won"] - 1
    data[name]["hands_won"] = update_wins

    # Save the updated data back to the ledger.json file
    with open("secrets/ledger.json", "w") as f:
        json.dump(data, f, indent=4)

    message = f"Removed one win to Player {name}\n" f"Total Wins: {update_wins}\n"

    await ctx.send(message)


@ledger.command()
async def addloss(ctx, name: str):
    # Load existing data from the ledger.json file
    try:
        with open("secrets/ledger.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist, initialize data as an empty dictionary
        data = {}

    # Check if the player with the given name already exists
    if name not in data:
        return await ctx.send(f"Player {name} does not exist!")

    update_loss = data[name]["hands_lost"] + 1
    data[name]["hands_lost"] = update_loss

    # Save the updated data back to the ledger.json file
    with open("secrets/ledger.json", "w") as f:
        json.dump(data, f, indent=4)

    message = f"Added one win to Player {name}\n" f"Total Wins: {update_loss}\n"

    await ctx.send(message)


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
        return await ctx.send(f"Player {name} does not exist!")

    # Check if player has more than 0 losses in order to remove one
    if data[name]["hands_lost"] == 0:
        return await ctx.send(f"Player {name} has 0 losses. Cannot remove loss!")

    # Check if hands_lost = 0 because we cannot go negative
    if data[name]["hands_lost"] <= 0:
        return await ctx.send(
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

    await ctx.send(message)


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
        return await ctx.send(f"Player {name} does not exist!")

    update_folds = data[name]["folds"] + 1
    data[name]["folds"] = update_folds

    # Save the updated data back to the ledger.json file
    with open("secrets/ledger.json", "w") as f:
        json.dump(data, f, indent=4)

    message = f"Added one win to Player {name}\n" f"Total Wins: {update_folds}\n"

    await ctx.send(message)


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
        return await ctx.send(f"Player {name} does not exist!")

    # Check if folds = 0 because we cannot go negative
    if data[name]["folds"] <= 0:
        return await ctx.send(
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

    await ctx.send(message)


bot.add_application_command(ledger)
bot.run(secrets["TOKEN"])
