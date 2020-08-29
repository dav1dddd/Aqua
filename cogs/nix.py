from discord import Embed
from discord.ext import commands
from aiohttp import ClientSession
from json import dump, load
from datetime import datetime

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
        nixos_repo = "https://api.github.com/users/NixOS"
        async with ClientSession() as session:
            async with session.get(nixos_repo) as response:
                if (response.status == 200):
                    json = await response.json()
                    
                    # Write this data to a file so it can be easily parsed and accessed.
                    # The with statement will automatically close the file, so we don't have to do anything.
                    with open("nixos.json", "w", encoding="UTF-8") as f:
                        dump(json, f, indent=4)
                    
                    # Now, the data can be read from the JSON file we just wrote to. The load() method is used this time.
                    with open("nixos.json", "r") as f:
                        data = load(f)
                        # Now, we can parse whatever we want from the file object.
                        name = data["login"]
                        description = data["name"]
                        avatar_url = data["avatar_url"]
                        website = data["blog"]
                        repos = data["public_repos"]

                        await ctx.send(
                            embed=Embed(
                                title=name,
                                description=description,
                                colour=0x7DCEA0,
                            )
                            .add_field(name="Repositories", value=repos, inline=True)
                            .add_field(name="Website", value=website, inline=True)
                            .set_thumbnail(url=avatar_url)
                            .set_footer(text=f"Created at | {datetime.now().strftime('%d.%m.%Y')}")
                        )

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
