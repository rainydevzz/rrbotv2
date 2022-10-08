import discord
from discord.ext import commands
from uistuff import errorui

class ErrorHandler(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(errorui.ErrorView())

    @discord.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        gu = self.bot.get_guild(994933726704320534)
        e1 = discord.utils.get(gu.emojis, name="menhera_oops")
        e2 = discord.utils.get(gu.emojis, name="catcri")
        if isinstance(error, commands.MissingPermissions):
            return await ctx.respond(f"you do not have permission to run this command. {e2}", ephemeral=True)
        
        em = discord.Embed(
            title=f"Oh No! An error occured... {e1}",
            description=f"```{error}```\n\nFeel free to ping Rainy so he knows about the issue.",
            color=discord.Color.embed_background(theme='dark')
        )

        await ctx.respond(embed=em, view=errorui.ErrorView())

def setup(bot):
    bot.add_cog(ErrorHandler(bot))