import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
import os
from dotenv import load_dotenv

# Chargement du token depuis une variable d'environnement ou un fichier .env
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD")
if GUILD_ID is None:
    raise ValueError("La variable d’environnement 'GUILD' est manquante.")
GUILD_ID = int(GUILD_ID)

# Intégration au bot
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Événement on_ready + synchronisation slash
@bot.event
async def on_ready():
    guild = discord.Object(id=int(GUILD_ID))
    await bot.tree.sync(guild=guild)  # synchronisation pour ton serveur uniquement
    print(f"✅ Connecté en tant que {bot.user}")
    print(f"✅ Commandes slash synchronisées pour le serveur : {GUILD_ID}")

# Chargement des extensions (dossier "commands/")
@bot.event
async def setup_hook():
    for filename in os.listdir("./commands"):
        if filename.endswith(".py"):
            await bot.load_extension(f"commands.{filename[:-3]}")
            print(f"🔁 Extension chargée : {filename}")

bot.run(TOKEN)
