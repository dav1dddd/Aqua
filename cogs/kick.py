from discord import Embed
from discord.ext import commands

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="kick",
        description="Kick a guild member"
    )
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, reason=None): 
        # why would anyone do this though lol
        if member == ctx.message.author:
            await ctx.send("You can't kick yourself..")
 
        # Reason
        if reason == None:
            reason = "no reason"

        # Message to user
        msgtouser = Embed(
                    title=f"You were kicked from {ctx.guild.name} for {reason}."
                )
        await member.send(embed=msgtouser)

        # Kick
        kickembed = Embed(
                    title=f"{member} was kicked!"
                )
        await member.kick(reason=reason)
        await ctx.send(embed=kickembed)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to tag a member! ⚠️")

def setup(bot):
    bot.add_cog(Kick(bot))
