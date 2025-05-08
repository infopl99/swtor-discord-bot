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
if GUILD_ID is None:
    raise ValueError("La variable d’environnement 'GUILD' est manquante.")
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
    logger.info(f"Connecté en tant que {bot.user}")
    try:
        synced = await bot.tree.clear_commands(guild=None)  # vide les commandes globales
        synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))  # pour le serveur actuel
        synced = await bot.tree.sync()  # pour synchroniser globalement
        logger.info("Commandes synchronisées.")
        logger.info(f"{len(synced)} commandes synchronisées avec succès.")
    except Exception as e:
        logger.info(f"Erreur de synchronisation des commandes : {e}")

bot.run(TOKEN)
