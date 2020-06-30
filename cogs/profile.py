from discord import Embed, Member
from discord.ext import commands

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def profile(self, ctx, member: Member=None):
        # Check if member was given, if not return your profile info
        if member == None:
            member = ctx.message.author

        # Get our profile information
        profile = Embed(
            title="Profile ✨",
            type="rich",
            colour=0xb34df5,
        )
        profile.add_field(name="Name", value=member.name, inline=False)
        profile.add_field(name="ID", value=member.id, inline=False)
        profile.add_field(name="Status", value=member.status, inline=False)
        profile.add_field(name="Activity", value=member.activities, inline=False)
        profile.add_field(name="Created at", value=member.created_at, inline=False)
        profile.add_field(name="Joined  at", value=member.joined_at, inline=False)
        await ctx.send(embed=profile)

def setup(bot):
    bot.add_cog(Profile(bot))