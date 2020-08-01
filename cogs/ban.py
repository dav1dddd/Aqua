from discord import Member, Embed
from discord.ext import commands
from datetime import date

class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="ban",
        description="Bans a guild member and stores in banlist (until unbanned)"
    )
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member: Member, reason=None):
        if member == ctx.message.author:
            await ctx.send("You cannot ban yourself.")
    

        if reason == None:
            reason = "No reason"
        
        banmessage = Embed(
            title=f"You were banned in **{ctx.guild.name}** for **{reason}**",
        )
        await member.send(embed=banmessage)

        banembed = Embed(
           title=f"Banned {member} 🔨" 
        )
        await member.ban(reason=reason)
        await ctx.send(embed=banembed)

        await self.bot.database.execute(
            """
            CREATE TABLE IF NOT EXISTS banlist(id serial PRIMARY KEY, name text, banned text)
            """
        )

        await self.bot.database.execute(
            """
            INSERT INTO banlist(name, banned) VALUES($1, $2)
            """,
            member.name, date.today().strftime('%d/%m/%Y')
        )

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You must specify the member/ID to ban ⚠️")

def setup(bot):
    bot.add_cog(Ban(bot))