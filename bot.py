# Discord
import discord
from discord.ext import commands

# .env
from dotenv import load_dotenv
load_dotenv()

# misc
import os
import random

# sentry
import sentry_sdk
sentry_sdk.init(os.getenv("SENTRY_DSN"))

# db
from db import db

bot = commands.Bot(command_prefix="]", activity=discord.Game(name="made by dps#7551"))

# Load cogs
for c in os.listdir(path=f"./cogs"):
    # Check if files end with .py
    if c.endswith(".py"):
        # Split .py, then remove .py and get only the 'root' and not the 'ext'
        split = os.path.splitext(c)[0]
        # Append "cogs." to filename, and load the cogs :D
        bot.load_extension(f"cogs.{split}")

# Load events
for e in os.listdir(path=f"./events"):
    # Check if files end with .py
    if e.endswith(".py"):
        # Split .py, then remove .py and get only the 'root' and not the 'ext'
        split = os.path.splitext(e)[0]
        # Append "events." to filename, and load the events :D
        bot.load_extension(f"events.{split}")

# Connect to the Discord API
if __name__ == "__main__":
	bot.run(os.getenv("TOKEN"))
