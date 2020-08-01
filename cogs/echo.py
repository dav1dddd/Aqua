from discord.ext import commands
class Echo(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(
		name="echo",
		description="Sends whatever text you specify",
		aliases=["text"]
	)
	async def echo(self, ctx, *, message: str):
		await ctx.send(message)

	@echo.error
	async def echo_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument): 
			return

def setup(bot):
	bot.add_cog(Echo(bot))
