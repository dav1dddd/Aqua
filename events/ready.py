from discord import __version__
from discord.ext import commands
class Ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} is ready. Using discord.py version {__version__}.")
        print(f"Cogs: {[(i) for i in self.bot.cogs]}")

def setup(bot):
    bot.add_cog(Ready(bot))
