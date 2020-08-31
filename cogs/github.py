from discord import Embed
from discord.ext import commands
from aiohttp import ClientSession
from datetime import datetime
from asyncio import TimeoutError

api_url = "https://api.github.com/"
users = "https://api.github.com/users/"
user_repos = "https://api.github.com/repos/"

class GitHub(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="GitHub",
        description="View profiles, search repositories etc",
        aliases=["git"]
    )

    async def git(self, ctx, *args: str):
        if not args:
            await ctx.send(
                "You need to include some arguments for this to do anything. Here is what's possible as of now. `user`, `repo`"
            )
            return
        elif args[0] == "user":
            url = f"{users}{args[1]}"
        elif args[0] == "search":
            url = f"{user_repos}{args[1]}"
        else:
            return
        # Search for a GitHub user.
        async def request():
            async with ClientSession(headers={"Accept": "application/vnd.github.v3+json"}) as session:
                async with session.get(url) as response:
                    print(await response.json())
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

                    githubuserembed = await ctx.send(
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

                    # Now I am going to ask the user if they want to see a user, or a repository from the user.
                    # Probably going to change this but idk

                    reactions = ["👨‍🦲", "🔎"]
                    
                    # Check if embed was reacted to
                    def check(user, reaction):
                        return user == ctx.message.author and str(reaction.emoji) in reactions
                        
                    # Wait for websocket event ("message") to be dispatched
                    try:
                        await self.bot.wait_for("reaction_add", check=check, timeout=60)
                    except TimeoutError:
                        await ctx.send("You didn't react on time.")

                    for i in reactions:
                        await githubuserembed.add_reaction(i)
            
        await request()
        

    @git.error
    async def git_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(embed=Embed(
                title="⚠️ Couldn't find that user on GitHub.",
                colour=0xec7063
            ))

def setup(bot):
    bot.add_cog(GitHub(bot))