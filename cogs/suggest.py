import discord

from datetime import datetime
from discord.ext import commands

class Suggest(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def suggest(self, ctx, suggestion):
        em = discord.Embed(title=f"Suggestion From {ctx.author}", description=suggestion)
        em.set_footer(text="Suggestion", icon_url=ctx.author.avatar.url)
        em.timestamp = datetime.now()
        await ctx.respond("Suggestion Sent!", ephemeral=True)
        
        rn = ctx.guild.get_member(941778098674892851)
        await rn.send(embed=em)