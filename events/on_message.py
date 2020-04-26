from discord.ext import commands

class Message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        print("message was sent: ", msg.content)

def setup(bot):
    bot.add_cog(Message(bot))
