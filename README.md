# Poker Ledger Discord Bot

The inspiration for this bot was so that my friends and I can play the game of poker without actually betting real money (because we are broke college students). With this bot, we are able to use fake money to buy into game sessions, update our balance at the end of the session, and all while keeping a zero-sum game. We also currently have individual statistics and a leaderboard that displays everyone's progress throughout the game sessions we have, but are looking to add more statistics later.

# Would you like to improve the bot?

Hello! Here is what you need to do if you would like to improve the Ledger Bot.

## Adding the Bot to your server

### Requirements
- Discord Account
- Python3
- pip

### Step 1 - Fork Repository and Set Up Structure

First, fork this repository, following GitHub's instructions, into your own directory.
- On your local machine, in the main project directory, create a `secrets` folder.
- Create a file called `secrets.json` with the following structure:

```
{
    "TOKEN": "[insert token here]"
}
```

### Step 3 - Getting Developer Token

Then, go to the [Discord Developer Portal](https://discord.com/developers/applications) and follow these steps:
- Create a new bot application (button at the top-right of the screen) and name it whatever you would like
- Go into the application you made
- Go to the `Bot` tab and click on `Reset Token`
    - You might need to provide your GitHub credentials.
- Copy the token and paste it into the `"TOKEN"` field of the `secrets/secrets.json` file

### Step 4 - Setting up Virtual Environment

Open up terminal and stay in the project root directory.
- Create virtual environment:
```
python3 -m venv bot-env
```
- Start the virtual environment:
```
source bot-env/bin/activate
```
- Install the requirements mentioned in `requirements.txt`
```
pip install -r requirements.txt
```

### Step 5 - Adding Bot to Server
Now, on Discord, create a Test Server of your own. Then, go back to the [Discord Developer Portal](https://discord.com/developers/applications) and follow these steps:
- Go into your application
- Go to the `Installation` tab
- Check `Guild Install`
- In the `Install Link` dropdown, use a `Discord Provided Link` and go to the link given.
- From here, Discord should instruct you on how to add the bot to your Test Server.

### Final Step - Activating Bot
Open up terminal on your project main directory and type the command
```
python3 bot.py
```

This starts the Discord Ledger Bot and you will be able to play with the commands in your own Test Server!

## Developing an Improvement - Pull Request

If you would like to provide an improvement or change to the bot, publish your own branch, commit to it, and provide a PR describing the addition. I will review the PR and merge the branch if good.

## Useful Links
- [PyCord Guide](https://guide.pycord.dev/)
- [Pretty Print Messages Resources](https://plainenglish.io/blog/python-discord-bots-formatting-text-efca0c5dc64a)
