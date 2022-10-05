import discord
import aiohttp

class Quotes(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_quote(self):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.quotable.io/random") as resp:
                if resp.status == 200:
                    data = await resp.json(content_type=None)
                    return data
                else:
                    return None

    @discord.slash_command()
    async def quote(self, ctx):
        q = await self.get_quote()
        if not q:
            return await ctx.respond("A quote could not be retrieved. Try again later.")
        em = discord.Embed(title="Quote For You! <3", description=f"**{q['content']}**", color=discord.Color.random())
        em.set_footer(text=f"{q['author']}")

        await ctx.respond(embed=em)

def setup(bot):
    bot.add_cog(Quotes(bot))