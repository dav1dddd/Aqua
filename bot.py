# Discord
from asyncpg import create_pool
from asyncio import get_event_loop
import random
from os import getenv, listdir, path
from discord import Status, Game, Intents
from discord.ext import commands

# .env
from dotenv import load_dotenv
load_dotenv()

# Default prefix
default_prefix = "!"

class CustomBot(commands.Bot):
    def __init__(self):
        # self.activity = Game(name="made by davidd#7551")
        self.status = Status.idle
        # Call superclass commands.Bot. Equal to commands.Bot(command_prefix=self.get_prefix)
        super().__init__(
            command_prefix=self.get_prefix_,
            # activity=self.activity,
            status=self.status,
            intents=Intents.all()
        )

        self.database = get_event_loop().run_until_complete(
            # ElephantSQL free tier only has a max pool size of 5, so the pool 
            # size needs to be set manually.
            create_pool(getenv("DB_URL"), min_size=1, max_size=2)
        )
        # self.database is allocated to postgresql database

    async def get_prefix_(self, bot, message):
        guild_prefix = await self.database.fetchrow(
            """
            SELECT prefix
            FROM guilds 
            WHERE guild_id = $1
            """,
            message.guild.id
        )

        if guild_prefix is None:
            await self.database.execute(
                """
                INSERT INTO guilds (guild_id, prefix)
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

# Bot rich presence

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
