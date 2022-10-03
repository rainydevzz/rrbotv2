import discord
from discord.ext import commands

class ErrorHandler(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            return await ctx.respond("you do not have permission to run this command. :c")
        
        em = discord.Embed(
            name="Oh No! An error occured :c",
            description=error,
            color=discord.Color.embed_background(theme='dark')
        )

        await ctx.respond(embed=em)

def setup(bot):
    bot.add_cog(ErrorHandler(bot))