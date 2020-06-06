from discord.ext import commands
class Ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} is ready. Using discord.py version {self.discord.__version__}")

def setup(bot):
    bot.add_cog(Ready(bot))
