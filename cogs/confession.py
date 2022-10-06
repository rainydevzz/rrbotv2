import discord
import aiosqlite
import asyncio

from datetime import datetime
from discord.ext import commands

class Confession(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    conf = discord.SlashCommandGroup(name="confessions", description="confession commands")

    @discord.Cog.listener()
    async def on_ready(self):
        setattr(self.bot, "db", await aiosqlite.connect("main.sqlite"))
        await asyncio.sleep(1)
        async with self.bot.db.cursor() as cur:
            await cur.execute("CREATE TABLE IF NOT EXISTS confessions (channel INTEGER, count INTEGER, guild INTEGER, logchannel INTEGER)")
        await self.bot.db.commit()

    @conf.command(name="setup")
    @commands.has_permissions(manage_guild=True)
    async def csetup(self, ctx, channel:discord.TextChannel, logchannel:discord.TextChannel):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT channel FROM confessions WHERE guild = ?", (ctx.guild.id,))
            res = await cursor.fetchone()
            if not res:
                await cursor.execute("INSERT INTO confessions (channel, count, guild, logchannel) VALUES (?, ?, ?, ?)", (channel.id, 1, ctx.guild.id, logchannel.id))
            else:
                await cursor.execute("UPDATE confessions SET channel = ?, logchannel = ? WHERE guild = ?", (channel.id, logchannel.id, ctx.guild.id))
        await self.bot.db.commit()
        await ctx.respond("Confessions Set Up! <3")

    @conf.command(name="confess")
    async def confess(self, ctx, confession):
        async with self.bot.db.cursor() as cur:
            await cur.execute("SELECT channel, logchannel, count FROM confessions WHERE guild = ?", (ctx.guild.id,))
            res = await cur.fetchone()
            if res is None:
                return await ctx.respond("The confession channel has not been set up. :(", ephemeral=True)

            elif c1 != ctx.channel.id:
                return await ctx.respond("This is not the confession channel. :c", ephemeral=True)

            c1, c2, co = res[0], res[1], res[2]
            
            em1 = discord.Embed(title=f"Confession {co}", description=confession, color=discord.Color.random())
            em1.timestamp = datetime.now()
            em1.set_footer(text="Confession!")
            em2 = discord.Embed(title=f"Confession Log From {ctx.author}", description=confession, color=discord.Color.embed_background(theme='dark'))
            em2.timestamp = datetime.now()
            em2.set_footer(text="Confession!")
            logc = self.bot.get_channel(c2)

            await cur.execute("UPDATE confessions SET count = ? WHERE guild = ?", (co + 1, ctx.guild.id))

            await ctx.channel.send(embed=em1)
            await logc.send(embed=em2)
            await ctx.respond("Confession Sent", ephemeral=True)

        await self.bot.db.commit()

def setup(bot):
    bot.add_cog(Confession(bot))