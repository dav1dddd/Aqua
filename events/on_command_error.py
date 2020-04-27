from discord.ext import commands

class HandleErrors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if error:
            await ctx.message.add_reaction("\N{CROSS MARK}")

    @commands.Cog.listener()
    async def on_command(self, ctx):
        await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")

def setup(bot):
    bot.add_cog(HandleErrors(bot))
