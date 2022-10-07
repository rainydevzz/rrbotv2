import discord
from discord.ui import View

class ErrorView(View): 
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Ping Rainy", style=discord.ButtonStyle.green, custom_id="accept-btn")
    async def acc_callback(self, button, interaction: discord.Interaction):
        rn = interaction.guild.get_member(941778098674892851)
        await interaction.response.send_message(f"Hey {rn.mention}, an error has occured.")
        self.disable_all_items()