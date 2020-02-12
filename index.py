import discord
from discord.ext import commands
import datetime

bot = commands.Bot(command_prefix="!", activity=discord.Game(name="made by dps#0001"))

# Events
@bot.event
async def on_ready():
	print(f"{bot.user} is ready. d.py version: {discord.__version__}")

@bot.event
async def on_message(message):
	if message.author == bot.user:
		return

	print(message.author, message.content)
	
	print(f"{message.content}")
	# Fix commands not working because of overriding default on_message
	await bot.process_commands(message)

# Commands
@bot.command()
async def ping(ctx):
	await ctx.send(embed=discord.Embed(
		title=f":ping_pong: Latency: {bot.latency}",
		colour=0x00ffff
	))

@bot.command()
async def echo(ctx, *, message: str):
	await ctx.send(message)

# Connect to the Discord API
bot.run("Njc1Njg0NjgzNDcxOTEyOTYw.XkEwYQ.w6ZiG_dCebxSwoBmmEO2mnESDEw")
