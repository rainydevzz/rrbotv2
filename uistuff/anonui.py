import discord
import aiosqlite

from discord.ui import View, Modal

class AnonView(View): #class for applying
    def __init__(self, db):
        self.db = await aiosqlite.connect('main.sqlite')
        super().__init__(timeout=None)
    @discord.ui.button(label="Report", custom_id="apply-button", style=discord.ButtonStyle.red)
    async def btn_callback(self, button, interaction: discord.Interaction):
        async with self.db.cursor() as cur:
            await cur.execute("SELECT channel FROM anon WHERE guild = ?", (interaction.guild_id,))