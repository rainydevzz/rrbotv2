import discord
import aiosqlite

from discord.ui import View, Modal
from cogs.anon.Anonymous import bot

class AnonView(View): #class for applying
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Report", custom_id="apply-button", style=discord.ButtonStyle.red)
    async def btn_callback(self, button, interaction: discord.Interaction):
        gid = int(interaction.message.embeds[0].fields[0].value)
        cnt = interaction.message.embeds[0].description
        modal = Modal(title="Report")
        modal.add_item(InputText(label="Reason", style=discord.InputTextStyle.long))
        async with bot.db.cursor() as cur:
            await cur.execute("SELECT channel FROM anon WHERE guild = ?", (gid,))
            res = await cur.fetchone()
            if not res:
                return await interaction.response.send_message("A report channel has not been set up.")
            
        channel = interaction.guild.get_channel(res[0])
        async def modal_callback(inter:discord.Interaction):
            reason = modal.children[0].value
            em = discord.Embed(title=f"Report From {inter.user}", description=reason)
            em.add_field(name="Content", value=cnt)
            await channel.send(embed=em)
            await inter.response.send_message("Thank you for your time. Your report will be evaluated.")
            
        modal.callback = modal_callback
        await interaction.response.send_modal(modal)
        await modal.wait()