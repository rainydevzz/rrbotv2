import discord
import aiohttp
import aiosqlite

from discord.ext import commands

class Plural(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def toWebhook(self, wurl, content):
        async with aiohttp.ClientSession() as cs:
            webhook = discord.Webhook.from_url(url=wurl, session=cs)
            await webhook.send(content)

    pcmd = discord.SlashCommandGroup(name="plural", description="plural cmds")

    @discord.Cog.listener()
    async def on_ready(self):
        setattr(self.bot, 'db', await aiosqlite.connect('main.sqlite'))
        async with self.bot.db.cursor() as cur:
            await cur.execute("CREATE TABLE IF NOT EXISTS plural (prefix TEXT, url TEXT, guild INTEGER, user INTEGER)")
            await cur.execute("CREATE TABLE IF NOT EXISTS pluraladmin (guild INTEGER, user INTEGER)")
        await self.bot.db.commit()

    @pcmd.command(description="adds a user to the trusted database.")
    @commands.has_permissions(manage_guild=True)
    async def add(self, ctx, user:discord.Member):
        async with self.bot.db.cursor() as cur:
            await cur.execute("SELECT user FROM pluraladmin WHERE guild = ? AND user = ?", (ctx.guild.id, user.id))
            res = await cur.fetchone()
            if res:
                return await ctx.respond("This user has already been added.")
            await cur.execute("INSERT INTO pluraladmin (guild, user) VALUES (?, ?)", (ctx.guild.id, user.id))
            await ctx.respond(f"{user.mention} added to the database. <3")

    @pcmd.command(description="removes a user from the trusted database.")
    @commands.has_permissions(manage_guild=True)
    async def remove(self, ctx, user:discord.Member):
        async with self.bot.db.cursor() as cur:
            await cur.execute("DELETE FROM pluraladmin WHERE guild = ? AND user = ?", (ctx.guild.id, user.id))
            await cur.execute("DELETE FROM plural WHERE user = ? AND guild = ?", (user.id, ctx.guild.id))
        await self.bot.db.commit()
        await ctx.respond("User removed if they were in the database.")

    @pcmd.command(description="Creates a plural user. Ask an admin for the channel you should set it to!")
    async def create(self, ctx, name, prefix, channel:discord.TextChannel):
        async with self.bot.db.cursor() as cur:
            await cur.execute("SELECT user FROM pluraladmin WHERE guild = ? AND user = ?", (ctx.guild.id, ctx.author.id))
            res = await cur.fetchone()
            if res is None:
                return await ctx.respond("You are not in the trusted user database.", ephemeral=True)
            
            wh = await channel.create_webhook(name=name)
            await cur.execute("INSERT INTO plural (user, prefix, url, guild) VALUES (?, ?, ?, ?)", (ctx.author.id, prefix, wh.url, ctx.guild.id))

            await ctx.respond("Successfully created a webhook user. <3", ephemeral=True)

        await self.bot.db.commit()

    @discord.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        async with self.bot.db.cursor() as cur:
            await cur.execute("SELECT user FROM pluraladmin WHERE guild = ? AND user = ?", (message.guild.id, message.author.id))
            check = await cur.fetchone()
            if check is None:
                return

            await cur.execute("SELECT user, prefix, url FROM plural WHERE guild = ?", (message.guild.id,))
            res = await cur.fetchone()
            if res is not None:
                user, prefix, url = res[0], res[1], res[2]
                if message.author.id == user and message.content.startswith(prefix):
                    cnt = message.content.split(prefix)[1]
                    await message.delete()
                    await self.toWebhook(wurl=url, content=cnt)

def setup(bot):
    bot.add_cog(Plural(bot))