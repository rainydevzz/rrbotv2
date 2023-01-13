import discord
from discord.ext import commands

class Utils(discord.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.unverified = 1021569052952514605
        self.ages = [
            1021569052809908252,
            1021569052809908251,
            1021569052809908250,
            1021569052809908249,
            1023595806512656475
        ]
        self.prns = [
            1021569052767961099,
            1021569052767961098,
            1021569052721811525,
            1021569052721811522,
            1021569052721811524,
            1021569052721811523,
            1021569052721811521
        ]

    @discord.slash_command(name="check-kick", description="check for users to kick or ask for roles!")
    @commands.has_permissions(moderate_members=True)
    async def check_kick(self, ctx):
        await ctx.defer()
        memstr = "**Missing Roles**\n"
        for mem in ctx.guild.members:
            if mem.bot: continue
            for role in mem.roles:
                if role.id in self.ages or role.id in self.prns and not role.id == self.unverified:
                    break
                else:
                    continue
            else:
                memstr += f"{mem.name}#{mem.discriminator}\n"

        mem2 = "**Unverified**\n"
        for mem in ctx.guild.members:
            rids = [r.id for r in mem.roles]
            if self.unverified in rids:
                mem2 += f"{mem.name}#{mem.discriminator}\n"

        await ctx.respond(f"{memstr}\n{mem2}")

def setup(bot):
    bot.add_cog(Utils(bot))