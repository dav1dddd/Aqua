from discord import Embed
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(embed=Embed(
            title=f":ping_pong: {self.bot.latency}"
            ))

def setup(bot):
    bot.add_cog(Ping(bot))
