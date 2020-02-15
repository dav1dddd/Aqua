import discord
from discord.ext import commands
import datetime

bot = commands.Bot(command_prefix="!", activity=discord.Game(name="made by dps#0001"))

# Events
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    print(message.author, message.content)
 
    print(f"{message.content}")
    # Fix commands not working because of overriding default on_message
    await bot.process_commands(message)

    if message.content.startswith("test"):
        await message.channel.send("hello")

# Load cogs
cogs = ["cogs.ping"]
for c in cogs: 
    bot.load_extension(c)

# Load events
events = ["events.ready"]
for e in events:
    bot.load_extension(e)

# Commands  

@bot.command()
async def echo(ctx, *, message: str):
    await ctx.send(message)

# Connect to the Discord API
bot.run("Njc1Njg0NjgzNDcxOTEyOTYw.XkfaXg.KDjI_qsu4dy7tCrZ5qZm57NFLKk")
