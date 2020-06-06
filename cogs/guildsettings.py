from discord import Embed
from discord.ext import commands
from asyncio import TimeoutError

class guildSettings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="guildsettings",
        description="Settings for your guild",
        aliases=["settings"]
    )
    async def guildSettings(self, ctx):
        settingsEmbed = Embed(
            title="Settings ✨",
            description="Settings for this guild",
            colour=0xA600FF
        )
        settingsEmbed.add_field(name="Prefix", value="🔧", inline=True)
        settingsEmbed.add_field(name="Logs", value="📜", inline=True)
        settingsEmbed.add_field(name="Roles", value="🌿", inline=True)
        settingsEmbed.add_field(name="Eval", value="⚠️", inline=True)
    
        msg = await ctx.send(embed=settingsEmbed)
        reactions = ["🔧", "📜", "🌿", "⚠️"]
        
        # For items in list, add reaction to embed.
        for i in reactions:
            await msg.add_reaction(i)

        # Check if emoji is reacted to.
        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) == "📜"

        # Wait for reaction then do something once reacted.
        try:
            reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=60.0)
        except TimeoutError:
            await ctx.send("You didn't react on time")
        else:
            print(f"{user} reacted with {reaction}")

            inputEmbed = Embed(
                title="Enter the ID of your log channel. This will be added to the database",
            )

            await ctx.send(embed=inputEmbed)
            channel_id = await self.bot.wait_for("message")

            # Create table and add channel ID to database. This can be fetched in on_member_join or another event (for sending logs to a different channel).
            db = self.bot.database
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS logs(
                    id serial PRIMARY KEY,
                    logchannel bigint
                )
                """
            )

            await db.execute(
                """
                INSERT INTO logs(logchannel)
                VALUES ($1)
                """,
                int(channel_id.content)
            )

            await ctx.send("Channel ID has been added to database! ✨")

def setup(bot):
    bot.add_cog(guildSettings(bot))