from discord import Embed
from discord.ext import commands
import aiohttp

class Neko(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def neko(self, ctx):
		c = aiohttp.ClientSession()
		async with c as s:
			async with s.get("https://nekos.life/api/v2/img/neko") as response:
				restxt = await response.json()
				neko_UwU = restxt["url"]
				
				# Make a new embed :3
				embed = Embed(
					title="A cute neko :3",
					colour=0x9b59b6
				)
				
				embed.set_image(url=neko_UwU)
				await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Neko(bot))
