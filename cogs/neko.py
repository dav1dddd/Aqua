from discord import Embed
from discord.ext import commands
from aiohttp import ClientSession

class Neko(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def neko(self, ctx):
        async with ClientSession() as s:
            async with s.get("https://nekos.life/api/v2/img/neko") as r:
                if r.status == 200:
                    json = await r.json()
                    await ctx.send(embed=Embed(
                        title="Neko >w<"
                    ).set_image(url=json["url"]))
                else:
                    print(f"looks like there was an error :/. Here is the status code {r.status}")

def setup(bot):
    bot.add_cog(Neko(bot))
    