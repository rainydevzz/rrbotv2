import discord
import apraw
import random

from config import passwd, usern

red = apraw.Reddit(
    password=passwd,
    client_id = "KRLi09w4yg3OqsXEv9sDFQ",
    client_secret = "mE5K-ZC3xYBKGGLhTklPq37GpQeYXA",
    user_agent = "RainyPraw",
    username=usern
)

class RedditCog(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="Pulls an image from r/RoleReversal. Rerun if an issue is faced.")
    async def rrpic(self, ctx):
        await ctx.defer()
        nl = []
        subreddit = await red.subreddit("RoleReversal")
        top = subreddit.new(limit = 35)
        async for p in top:
            nl.append(p)
        ranpost = random.choice(nl)
        url = ranpost.url
        print(url)
        name = ranpost.title
        embed = discord.Embed(title=name, description="pulled from r/RoleReversal ^^\nRRBot is not responsible for the quality or content of images <3", color=0x800080)
        embed.set_image(url=url)
        embed.set_thumbnail(url=ranpost.thumbnail)
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(RedditCog(bot))