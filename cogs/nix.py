from discord import Embed
from discord.ext import commands
from aiohttp import ClientSession

class Nix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="nix",
        description="nix packages for Debian/Arch/RHEL based systems and macOS",
        aliases=["pkgs"],
    )
     
    async def fetch(client): 
        debianstable = "https://packages.debian.org/stable/allpackages"
        async with client.get(debianstable) as response:
            # Test if response is equal to 200.
            # Otherwise, AssertionError is raised.
            assert response.status == 200
            print(status)
            # Show the HTML of the website.
            return await response.text()

    async def nix(self, ctx):
        async with ClientSession() as client:
            print(await fetch(client))

def setup(bot):
    bot.add_cog(Nix(bot))
