from discord.ext import commands
class Echo(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def echo(self, ctx, *, message: str):
		await ctx.send(message)

def setup(bot):
	bot.add_cog(Echo(bot))
