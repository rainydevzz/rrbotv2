import discord
import asyncio
import aiosqlite
from uistuff.anonui import AnonView

class Anonymous(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.Cog.listener()
    async def on_ready(self):
        setattr(self.bot, "db", await aiosqlite.connect('main.sqlite'))
        await asyncio.sleep(1)
        async with self.bot.db.cursor as cur:
            await cur.execute("CREATE TABLE IF NOT EXISTS anon (channel INTEGER, guild INTEGER)")
        await self.bot.db.commit()
        await self.bot.add_view(AnonView())

    ancmd = discord.SlashCommandGroup(name="anonymessage", description="Send an anonymous message to a user of your choice. :3")

    @ancmd.command(name="send")
    async def a_send(self, ctx, message, user:discord.Member):
        em = discord.Embed(title="A message for you!", description=message)
        em.set_footer(text="Feel free to click report if this message contains upsetting content.")
        await user.send(embed=em, view=AnonView())

    @ancmd.command(name="setup")
    async def an_setup(self, ctx, channel:discord.TextChannel):
        async with self.bot.db.cursor() as cur:
            await cur.execute("INSERT INTO anon (channel, guild) VALUES (?, ?)", (channel.id, ctx.guild.id))
        await self.bot.db.commit()
        await ctx.respond(f"Anon Reports Log set to {channel.mention} <3")

def setup(bot):
    bot.add_cog(Anonymous(bot))