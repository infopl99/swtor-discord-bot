import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger("swtor_bot")
logging.basicConfig(level=logging.INFO)

# Chargement du token depuis une variable d'environnement ou un fichier .env
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD")
if GUILD_ID is not None:
    GUILD_ID = int(GUILD_ID)

# Intégration au bot
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Chargement des extensions (dossier "commands/")
@bot.event
async def setup_hook():
    for filename in os.listdir("./commands"):
        if filename.endswith(".py"):
            await bot.load_extension(f"commands.{filename[:-3]}")
            logger.info(f"🔁 Extension chargée : {filename}")

# Événement on_ready + synchronisation slash
@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")
    try:
        if GUILD_ID:
            synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
            print(f"✅ {len(synced)} commandes synchronisées pour le serveur {GUILD_ID}")
        else:
            synced = await bot.tree.sync()
            print(f"✅ {len(synced)} commandes globales synchronisées.")
    except Exception as e:
        print(f"❌ Erreur de synchronisation des commandes : {e}")

bot.run(TOKEN)
