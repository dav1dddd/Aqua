import discord
from discord.ext import commands
import datetime
from dotenv import load_dotenv
load_dotenv()
import os
import sentry_sdk
sentry_sdk.init(os.getenv("SENTRY_DSN"))

from db.db import Database

bot = commands.Bot(command_prefix="!", activity=discord.Game(name="made by dps#0001"))
bot.Database = Database()

# Load cogs
cogs = ["cogs.ping", "cogs.yiff", "cogs.neko", "cogs.echo"]
for c in cogs: 
    bot.load_extension(c)

# Load events
events = ["events.ready", "events.on_message"]
for e in events:
    bot.load_extension(e)

# Connect to the Discord API
if __name__ == "__main__":
	bot.run(os.getenv("TOKEN"))
