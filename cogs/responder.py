import discord
import asyncio
import aiosqlite
from discord.ext import commands

class Responder(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    rcmd = discord.SlashCommandGroup(name="responder", description="responder commands")

    @rcmd.command()
    async def rsetup(self, ctx, trigger_msg, response):
        pass

    @discord.Cog.listener()
    async def on_ready(self):
        setattr(self.bot, "db", await aiosqlite.connect("main.sqlite"))
        await asyncio.sleep(1)
        async with self.bot.db.cursor() as cur:
            await cur.execute("CREATE TABLE IF NOT EXISTS responder (guild INTEGER, channel INTEGER, trigger TEXT, response TEXT)")
        await self.bot.db.commit()