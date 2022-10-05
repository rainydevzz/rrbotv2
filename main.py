import discord
import os

from config import token

intents = discord.Intents.all()
bot = discord.Bot(intents=intents)

for files in os.listdir("./cogs"):
    if files.endswith(".py"):
        cogf = files[:-3]
        bot.load_extension(f"cogs.{cogf}")
        print(f"{cogf} initialized!")

@bot.event
async def on_ready():
    print("logged in")

bot.run(token)