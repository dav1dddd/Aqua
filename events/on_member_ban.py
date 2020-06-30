from discord import Embed, Member
from discord.ext import commands
from datetime import date

class onMemberBan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_ban(self, guild, member: Member, reason=None):
        db = self.bot.database

        if reason == None:
            reason = "No reason"
        # Embed with banned user and reason
        onmemberbanembed = Embed(
            title="Banned member ✅",
            type="rich",
        )
        onmemberbanembed.add_field(name="Name", value=member.name, inline=False)
        onmemberbanembed.add_field(name="ID", value=member.id, inline=False)
        onmemberbanembed.add_field(name="Reason", value=reason, inline=False)
        onmemberbanembed.set_thumbnail(url=member.avatar_url)
        onmemberbanembed.set_footer(
            text=date.today().strftime("%B %d, %Y")
        )

        # Get the log channel from database
        logChannelID = await db.fetchval(
            """
            SELECT logchannel FROM logs
            """
        )
        await self.bot.get_channel(logChannelID).send(embed=onmemberbanembed)

def setup(bot):
    bot.add_cog(onMemberBan(bot))
