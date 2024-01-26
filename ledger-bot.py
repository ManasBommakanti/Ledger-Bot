import discord
from discord.ext import commands
from discord.commands import Option

import json
import asyncio
import os

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
async def get_player_data(ctx) -> dict:
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

    return data["players"]


# Update data of Ledger System
async def update_player_data(ctx, data: dict):
    print(data)
    # Save the updated data back to the ledger.json file
    try:
        with open("secrets/ledger.json", "w") as f:
            json.dump({"players": data}, f, indent=4)
    except Exception as e:
        print(e)
        embed = discord.Embed(
            title="Error!",
            description=f"Something is wrong internally :(",
            color=discord.Colour.red(),
        )
        return await ctx.respond(embed=embed)


"""
UPDATE COMMAND FUNCTIONS
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
    data = await get_player_data(ctx)

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

    await update_player_data(ctx, data)

    embed = discord.Embed(
        title="Player Added!",
        description=f"Welcome **{name}**!",
        color=discord.Colour.dark_green(),
    )

    await ctx.respond(embed=embed)


@ledger.command(name="addwin", description="Add a win to yourself or another player")
async def addwin(ctx, member: discord.Member = None):
    name = await get_username(ctx, member)
    data = await get_player_data(ctx)

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

    await update_player_data(ctx, data)

    embed = discord.Embed(
        title=f"Updating Win",
        description=(
            f"*Added* one win to Player **{name}**!\n" f"Total Win(s): {update_wins}\n"
        ),
        colour=discord.Colour.green(),
    )

    await ctx.respond(embed=embed)


@ledger.command(
    name="removewin", description="Remove a win from yourself or another player"
)
async def removewin(ctx, member: discord.Member = None):
    name = await get_username(ctx, member)
    data = await get_player_data(ctx)

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
            description=f"Player **{name}** did not win anything :(\n"
            f"Cannot remove from 0 wins",
            color=discord.Colour.dark_red(),
        )
        return await ctx.respond(embed=embed)

    update_wins = data[name]["hands_won"] - 1
    data[name]["hands_won"] = update_wins

    await update_player_data(ctx, data)

    embed = discord.Embed(
        title=f"Updating Win",
        description=(
            f"*Removed* one win from Player **{name}**!\n"
            f"Total Win(s): {update_wins}\n"
        ),
        colour=discord.Colour.red(),
    )

    await ctx.respond(embed=embed)


@ledger.command(name="addloss", description="Add a loss to yourself or another player")
async def addloss(ctx, member: discord.Member = None):
    name = await get_username(ctx, member)
    data = await get_player_data(ctx)

    # Check if the player with the given name already exists
    if name not in data:
        embed = discord.Embed(
            title="Error!",
            description=f"Player with username **{name}** is not in Ledger System.",
            color=discord.Colour.dark_red(),
        )
        return await ctx.respond(embed=embed)

    update_loss = data[name]["hands_lost"] + 1
    data[name]["hands_lost"] = update_loss

    await update_player_data(ctx, data)

    embed = discord.Embed(
        title=f"Updating Loss",
        description=(
            f"*Added* one loss to Player **{name}**!\n"
            f"Total Loss(es): {update_loss}\n"
        ),
        colour=discord.Colour.red(),
    )

    await ctx.respond(embed=embed)


@ledger.command(
    name="removeloss", description="Remove a loss from yourself or another player"
)
async def removeloss(ctx, member: discord.Member = None):
    name = await get_username(ctx, member)
    data = await get_player_data(ctx)

    # Check if the player with the given name already exists
    if name not in data:
        embed = discord.Embed(
            title="Error!",
            description=f"Player with username **{name}** is not in Ledger System.",
            color=discord.Colour.dark_red(),
        )
        return await ctx.respond(embed=embed)

    # Check if player has more than 0 losses in order to remove one
    if data[name]["hands_lost"] <= 0:
        embed = discord.Embed(
            title="Error!",
            description=(
                f"Player **{name}** did not lose anything... yet\n"
                f"Cannot remove from 0 losses"
            ),
            color=discord.Colour.dark_red(),
        )
        return await ctx.respond(embed=embed)

    update_loss = data[name]["hands_lost"] - 1
    data[name]["hands_lost"] = update_loss

    await update_player_data(ctx, data)

    embed = discord.Embed(
        title=f"Updating Loss",
        description=(
            f"*Removed* one loss from Player **{name}**!\n"
            f"Total Loss(es): {update_loss}\n"
        ),
        colour=discord.Colour.green(),
    )

    await ctx.respond(embed=embed)


@ledger.command(name="addfold", description="Add a fold to yourself or another player")
async def addfold(ctx, member: discord.Member = None):
    name = await get_username(ctx, member)
    data = await get_player_data(ctx)

    # Check if the player with the given name already exists
    if name not in data:
        embed = discord.Embed(
            title="Error!",
            description=f"Player with username **{name}** is not in Ledger System.",
            color=discord.Colour.dark_red(),
        )
        return await ctx.respond(embed=embed)

    update_folds = data[name]["folds"] + 1
    data[name]["folds"] = update_folds

    await update_player_data(ctx, data)

    embed = discord.Embed(
        title=f"Updating Folds",
        description=(
            f"*Added* one fold to Player **{name}**!\n"
            f"Total Fold(s): {update_folds}\n"
        ),
        colour=discord.Colour.dark_gray(),
    )

    await ctx.respond(embed=embed)


@ledger.command(
    name="removefold", description="Remove a fold from yourself or another player"
)
async def removefold(ctx, member: discord.Member = None):
    name = await get_username(ctx, member)
    data = await get_player_data(ctx)

    # Check if the player with the given name already exists
    if name not in data:
        embed = discord.Embed(
            title="Error!",
            description=f"Player with username **{name}** is not in Ledger System.",
            color=discord.Colour.dark_red(),
        )
        return await ctx.respond(embed=embed)

    # Check if player has more than 0 losses in order to remove one
    if data[name]["folds"] <= 0:
        embed = discord.Embed(
            title="Error!",
            description=(
                f"Player **{name}** did not fold yet (idk how)\n"
                f"Cannot remove from 0 folds"
            ),
            color=discord.Colour.dark_red(),
        )
        return await ctx.respond(embed=embed)

    update_folds = data[name]["folds"] - 1
    data[name]["folds"] = update_folds

    await update_player_data(ctx, data)

    embed = discord.Embed(
        title=f"Updating Folds",
        description=(
            f"*Removed* one fold from Player **{name}**!\n"
            f"Total Fold(s): {update_folds}\n"
        ),
        colour=discord.Colour.dark_gray(),
    )

    await ctx.respond(embed=embed)


"""
DISPLAY COMMAND FUNCTIONS
"""


@ledger.command(
    name="individual_stats", description="Get your or another player's Poker stats"
)
async def individ_stats(ctx, member: discord.Member = None):
    name = await get_username(ctx, member)
    data = await get_player_data(ctx)

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


@ledger.command(name="leaderboard", description="Current Poker Leaderboard")
async def leaderboard(ctx):
    data = await get_player_data(ctx)

    # Calculate ratios and create a list of players with usernames and ratios
    player_ratios = [
        (username, player["hands_won"] / max(1, player["hands_lost"]))
        for username, player in data.items()
    ]

    # Sort the list based on ratios in descending order
    sorted_players = sorted(player_ratios, key=lambda x: x[1], reverse=True)

    message = ""

    # Iterate through all players
    for rank, (username, ratio) in enumerate(sorted_players, start=1):
        message += f"""{rank}. **{username}**
            Hands Won: {data[username]['hands_won']}
            Hands Lost: {data[username]['hands_lost']}
            W/L Ratio: {ratio}\n"""

    embed = discord.Embed(
        title="Leaderboard",
        description=message,
        colour=discord.Colour.blue(),
    )

    await ctx.respond(embed=embed)


"""
SETUP FUNCTIONS
"""


def setup_ledger():
    try:
        with open("secrets/ledger.json", "w") as f:
            json.dump({"players": {}}, f, indent=4)
    except Exception as e:
        print(e)

    print("INITIALIZED FILE secrets/ledger.json")


if __name__ == "__main__":
    if not os.path.exists("secrets/ledger.json"):
        setup_ledger()
    else:
        print("Ledger already set up")

    bot.add_application_command(ledger)
    bot.run(secrets["TOKEN"])
