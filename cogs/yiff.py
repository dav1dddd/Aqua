from discord import Embed
from discord.ext import commands
import aiohttp
from bs4 import BeautifulSoup

class Yiff(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def yiff(self, ctx):
		async with aiohttp.ClientSession() as s:
			async with s.get("https://e621.net/posts/random") as response:
				html = await response.text()
				
				# 🍲😋 soup object
				soup = BeautifulSoup(html, "html.parser")
				
				# Get image from meta tags
				image_meta = soup.find("meta", attrs={"name": "og:image"})
				image = image_meta["content"]
				
				# Send image to discord
				embed = Embed(
					title="A cute e621 image :3",
					colour=0x9b59b6,
						
				)
				embed.set_image(url=image)

				await ctx.send(embed=embed)				

def setup(bot):
	bot.add_cog(Yiff(bot))	
