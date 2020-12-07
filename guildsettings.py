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
            return user == ctx.message.author and str(reaction.emoji) in reactions

        # Wait for reaction then do something once reacted.
        try:
            reaction = await self.bot.wait_for("reaction_add", check=check, timeout=60.0)
        except TimeoutError:
            await ctx.send("You didn't react on time")
        else:
            db = self.bot.database
            # Prefix
            if str(reaction[0]) == reactions[0]:
                # Ask for prefix
                await ctx.send(embed=Embed(
                    title="Type in the prefix that you want"
                ))

                # Wait for websocket event
                prefix = await self.bot.wait_for("message")

                prefixval = await db.fetchrow(
                    """
                    SELECT prefix FROM guilds
                    WHERE guild_id = $1
                    """,
                    ctx.message.guild.id
                )

                # Update the prefix in the database with the prefix given
                if prefixval[0] == prefix.content:
                    await ctx.send("That prefix is already set.")
                else:
                    await db.execute(
                        f"""                        
                        UPDATE guilds SET prefix = $1 WHERE prefix = '{prefixval[0]}'
                        """,
                        str(prefix.content)
                    )

           
            # Logs
            if str(reaction[0]) == reactions[1]:
                # Logs 📜

                # Create table and add channel ID to database. This can be fetched in on_member_join or another event (for sending logs to a different channel).
                await db.execute(
                    """
                    CREATE TABLE IF NOT EXISTS logs(
                        id serial PRIMARY KEY,
                        guildID bigint,
                        logchannel bigint
                    )
                    """
                )

                # Check if the channel ID exists in the database
                # Send an embed if it does exist
                checkIfIDExists = await db.fetchrow(
                    """
                    SELECT logchannel FROM logs
                    WHERE guildID = $1
                    """,
                    ctx.message.guild.id
                )

                updateEmbed = Embed(
                    title="Would you like to update the log channel ID in your database?"
                )

                if checkIfIDExists:
                    IDreactions = await ctx.send(embed=updateEmbed)
                    await IDreactions.add_reaction("✅")
                    await IDreactions.add_reaction("❌")

                    # await db.execute(
                    #     """
                    #     UPDATE logs
                    #     SET logchannel = $2
                    #     WHERE guildID = $1
                    #     """,
                    #     ctx.message.guild.id,
                    #     int(update_channel_id.content)
                    # )
                    
                    await ctx.send("Channel ID has been updated ✨")
                else:
                    inputEmbed = Embed(
                        title="Enter the ID of your log channel. This will be added to the database",
                    )

                    await ctx.send(embed=inputEmbed)
                    
                    # Wait for websocket event "message"
                    channel_id = await self.bot.wait_for("message")

                    await db.execute(
                        """
                        INSERT INTO logs (guildID, logchannel)
                        VALUES ($1, $2)
                        """,
                        ctx.message.guild.id,
                        int(channel_id.content)
                    )

                    await ctx.send("Channel ID has been added to database! ✨")

def setup(bot):
    bot.add_cog(guildSettings(bot))
