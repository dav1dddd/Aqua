# Discord
import discord
from discord.ext import commands

# .env
from dotenv import load_dotenv
load_dotenv()

# misc
from os import getenv, listdir, path
import random

from asyncio import get_event_loop

# sentry
import sentry_sdk
dsn = getenv("SENTRY_DSN_KEY")
sentry_sdk.init(dsn)

# database
from asyncpg import create_pool

default_prefix = "!"

class CustomBot(commands.Bot):
    def __init__(self):
        # Call superclass commands.Bot. Equal to commands.Bot(command_prefix=self.get_prefix)
        super().__init__(
            command_prefix=self.get_prefix_, 
            activity=discord.Game(
                name="made by david.#7551"
                ), 
                status=discord.Status.idle
            )
        
        self.database = get_event_loop().run_until_complete(
            create_pool(getenv("DB_URL"))
        )
        # self.database is allocated to postgresql database

    async def get_prefix_(self, bot, message):
        guild_prefix = await self.database.fetchrow(
            """
            SELECT prefix
            FROM guilds 
            WHERE id = $1
            """, 
            message.guild.id
        )

        if guild_prefix is None:
            await self.database.execute(
                """
                INSERT INTO guilds (id, prefix)
                VALUES ($1, $2)
                """,
                message.guild.id,
                default_prefix
            )

            # Here we change the return value for prefix_for_guild.
            guild_prefix = {"prefix": default_prefix}

        return commands.when_mentioned_or(guild_prefix["prefix"])(bot, message)

# Instance of CustomBot
bot = CustomBot()

# Load cogs
for c in listdir(path=f"./cogs"):
    # Check if files end with .py
    if c.endswith(".py"):
        # Split .py, then remove .py and get only the 'root' and not the 'ext'
        split = path.splitext(c)[0]
        # Append "cogs." to filename, and load the cogs :D
        bot.load_extension(f"cogs.{split}")

# Load events
for e in listdir(path=f"./events"):
    # Check if files end with .py
    if e.endswith(".py"):
        # Split .py, then remove .py and get only the 'root' and not the 'ext'
        split = path.splitext(e)[0]
        # Append "events." to filename, and load the events :D
        bot.load_extension(f"events.{split}")

# # Connect to the Discord API
if __name__ == "__main__":
    t = getenv("TOKEN")
    bot.run(t)