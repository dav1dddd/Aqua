from discord.ext import commands

class Ping(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(
		name="ping",
		description="ping pong"
	)
	async def ping(self, ctx):
		await ctx.send("test")

def setup(bot):
	bot.add_cog(Ping(bot))
