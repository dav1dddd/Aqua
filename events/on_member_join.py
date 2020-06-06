from discord import Member, Guild, Embed
from discord.ext import commands

class onMemberJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        db = self.bot.database

        channel_id = await db.fetchval(
            """
            SELECT logchannel FROM logs
            """
        )

        joinembed = Embed(
            title="New member!",
            colour=0xA600FF,
        )
        joinembed.add_field(name="Username", value=f"{member.name}#{member.discriminator}", inline=False)
        joinembed.add_field(name="ID", value=f"{member.id}", inline=False)
        joinembed.add_field(name="Created at", value=f"{member.created_at}", inline=False)
        joinembed.add_field(name="Joined at", value=f"{member.joined_at}", inline=False)
        joinembed.set_thumbnail(url=member.avatar_url)

        await self.bot.get_channel(channel_id).send(embed=joinembed)

def setup(bot):
    bot.add_cog(onMemberJoin(bot))