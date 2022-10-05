import discord
import asyncio
import aiosqlite

class Tags(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.Cog.listener()
    async def on_ready(self):
        setattr(self.bot, "db", await aiosqlite.connect('main.sqlite'))
        await asyncio.sleep(1)
        async with self.bot.db.cursor() as cur:
            await cur.execute("CREATE TABLE IF NOT EXISTS tags (name TEXT, content TEXT, category TEXT, guild INTEGER)")
        await self.bot.db.commit()

    tcmd = discord.SlashCommandGroup(name="tags", description="tag commands")

    @tcmd.command()
    async def add(self, ctx, name, content, category):
        async with self.bot.db.cursor() as cur:
            await cur.execute(
                "INSERT INTO tags (name, content, category, guild) VALUES (?, ?, ?, ?)",
                (name.lower(), content, category.lower(), ctx.guild.id)
            )
        await self.bot.db.commit()
        await ctx.respond(f"tag {name} added! <3")

    @tcmd.command()
    async def view(self, ctx, name):
        async with self.bot.db.cursor() as cur:
            await cur.execute("SELECT content FROM tags WHERE guild = ? AND name = ?", (ctx.guild.id, name))
            res = await cur.fetchone()
            if not res:
                return await ctx.respond("no tag found.")
            content = res[0]
            await ctx.respond(content)

    @tcmd.command()
    async def viewall(self, ctx):
        async with self.bot.db.cursor() as cur:
            await cur.execute("SELECT name FROM tags WHERE guild = ?", (ctx.guild.id,))
            res = await cur.fetchall()
            tagList = []
            for r in res:
                tagList.append(r)
            em = discord.Embed(name="All Tags", description="".join(tagList, ", "))
        await ctx.respond(embed=em)

    @tcmd.command()
    async def viewcat(self, ctx, category):
        async with self.bot.db.cursor() as cur:
            await cur.execute("SELECT category, name FROM tags WHERE guild = ?", (ctx.guild.id,))
            res = await cur.fetchall()
            if not res:
                return await ctx.respond("No category by that name found.")
            cat = res[0][0]
            ls = []
            for r in res:
                tag = r[1]
                ls.append(tag)

            em = discord.Embed(name=f"Category: {cat}", description="".join(ls, ", "))
            await ctx.respond(embed=em)

    @tcmd.command()
    async def remove(self, ctx, tag):
        async with self.bot.db.cursor() as cur:
            await cur.execute("DELETE FROM tags WHERE name = ? AND guild = ?", (tag.lower(), ctx.guild.id))
        await self.bot.db.commit()
        await ctx.respond(f"Tag {tag} has been deleted if it existed. <3")