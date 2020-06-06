from discord import Member
from discord.ext import commands
class Chnick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="chnick", 
        description="Change nickname of other users",
        aliases=["nick"]
    )

    async def chnick(self, ctx, inp: str, member: Member):
        await member.edit(nick=inp)

    @chnick.error
    async def chnick_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send("The bot can't change your nickname because you are the owner; your role is higher than the bots role.")

def setup(bot):
    bot.add_cog(Chnick(bot))