from discord import __version__
from discord.ext import commands
class Ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        db = self.bot.database
        
        # Create table for prefix
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS guilds(id serial PRIMARY KEY, guild_id bigint, prefix text)
            """
        )

        prefix = await db.fetchval(
            """
            SELECT prefix FROM guilds
            """
        )

        print(f"{self.bot.user} is ready. Using discord.py version {__version__}.")
        print(f"Cogs: {[(i) for i in self.bot.cogs]}")
        print(await db.execute("SELECT * FROM guilds"))

def setup(bot):
    bot.add_cog(Ready(bot))
