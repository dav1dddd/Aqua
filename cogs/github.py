from discord import Embed
from discord.ext import commands
from aiohttp import ClientSession
from datetime import datetime

class GitHub(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="GitHub",
        description="View profiles, search repositories etc",
        aliases=["git"]
    )

    async def git(self, ctx, user=None):
        if user == None:
            return
        # Search for a GitHub user.
        async with ClientSession(headers={"Accept": "application/vnd.github.v3+json"}) as session:
            users = f"https://api.github.com/users/{user}"
            async with session.get(users) as response:
                json = await response.json()
                name = json["login"]
                avatar_url = json["avatar_url"]
                profile = json["html_url"]
                repos = json["public_repos"]
                gists = json["public_gists"]
                followers = json["followers"]
                following = json["following"]
                website = json["blog"]
                twitter = json["twitter_username"]
                
                if website == "":
                    website = None

                await ctx.send(
                        embed=Embed(
                            title="GitHub user",
                            colour=0x7DCEA0,
                        )
                        .add_field(name="Profile", value=f"[{name}]({profile})", inline=False)
                        .add_field(name="Repositories", value=repos, inline=True)
                        .add_field(name="Gists", value=gists, inline=True)

                        # Here I add an empty field as I want 2 rows with 2 columns
                        .add_field(name="\u200b", value="\u200b", inline=True)

                        .add_field(name="Following", value=following, inline=True)
                        .add_field(name="Followers", value=followers, inline=True)
                        .add_field(name="Website", value=website, inline=False)
                        .add_field(name="Twitter", value=twitter, inline=True)
                        .set_thumbnail(url=avatar_url)
                        .set_footer(text=f"Created at | {datetime.now().strftime('%d.%m.%Y')}")
                    )
def setup(bot):
    bot.add_cog(GitHub(bot))