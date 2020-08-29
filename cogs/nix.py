from discord import Embed
from discord.ext import commands
from aiohttp import ClientSession
from json import dump

status = []

class Nix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="nix",
        description="nix packages for Debian/Arch/RHEL based systems and macOS",
        aliases=["pkgs"]
    )

    async def nix(self, ctx):
        # Get the NixOS github JSON
        nixos_repo = "https://api.githu.com/users/NixOS"
        async with ClientSession() as session:
            async with session.get(nixos_repo) as response:
                if (response.status == 200):
                    json = await response.json()
                    
                    # Write this data to a file so it can be easily parsed and accessed.
                    # The with statement will automatically close the file, so we don't have to do anything.
                    with open("nixos.json", "w", encoding="UTF-8") as f:
                        dump(json, f, indent=4)

    # Use decorator to handle discordpy exception "CommandInvokeError"
    @nix.error
    async def nix_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError): # isinstance basically means "the same as"
            # Response should be 200, but if it isn't, let the user know.
            await ctx.send(embed=Embed(
                title="⚠️ Couldn't access the GitHub API. You can check the status [here](https://www.githubstatus.com).",
                colour=0xec7063
            ))

def setup(bot):
    bot.add_cog(Nix(bot))
