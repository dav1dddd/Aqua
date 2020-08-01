from discord import Member, Embed
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

        # Send message to member asking to verify via email.
        message = await member.send(
            content=f"Hello {member.name}, welcome to {member.guild}! You must verify via email to access the guild."
        )
        
        reactions = ["✅", "❌"]
        for i in reactions:
            await message.add_reaction(i)

        def check(r, u):
            return u == member.name and str(r.emoji) in reactions

        r, u = await self.bot.wait_for("reaction_add", check=check)
        if str(r.emoji) == reactions[0]:
            await member.send(content=f"You'll need to provide your email address so a verification code can be sent. ")
            email = await self.bot.wait_for("message")
            print(email.content)

        else:
            await member.send(content="Without verifying your email, you can't access any channels.")

        

def setup(bot):
    bot.add_cog(onMemberJoin(bot))