import discord

class Plural(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def toWebhook(webhookURL, content):
        async with aiohttp.ClientSession() as cs:
            webhook = discord.Webhook.from_url(webhookURL, session=cs)
            await webhook.send(content)

    pcmd = discord.SlashCommandGroup(name="plural", description="plural cmds")

    @discord.Cog.listener()
    async def on_ready(self):
        setattr(self.bot, 'db', await aiosqlite.connect('main.sqlite'))
        async with self.bot.db.cursor() as cur:
            await cur.execute("CREATE TABLE IF NOT EXISTS plural (prefix TEXT, url TEXT, guild INTEGER)")
            await cur.execute("CREATE TABLE IF NOT EXISTS pluraladmin (guild INTEGER, user INTEGER)")
        await self.bot.db.commit()

    @pcmd.command()
    @commands.has_permissions(manage_guild=True)
    async def add(self, ctx, user:discord.Member):
        async with self.bot.db.cursor() as cur:
            await cur.execute("SELECT user FROM integer WHERE guild = ? AND user = ?", (ctx.guild.id, user.id))
            res = await cur.fetchone()
            if res:
                return await ctx.respond("This user has already been added.")
            await cur.execute("INSERT INTO pluraladmin (guild, user) VALUES (?, ?)", (ctx.guild.id, user.id))
            await ctx.respond(f"{member.mention} added to the database. <3")

    @pcmd.command()
    @commands.has_permissions(manage_guild=True)
    async def remove(self, ctx, user:discord.Member):
        async with self.bot.db.cursor() as cur:
            await cur.execute("DELETE FROM pluraladmin WHERE guild = ? AND user = ?", (ctx.guild.id, user.id))
        await ctx.respond("User removed if they were in the database.")

    @pcmd.command()
    async def create(self, ctx, name, prefix):
        async with self.bot.db.cursor() as cur:
            await cur.execute("SELECT user FROM pluraladmin WHERE guild = ?", (ctx.guild.id,))
            res = await cur.fetchone()
            if not res:
                return await ctx.respond("You are not in the trusted user database.", ephemeral=True)
            # continue, create webhook, update db