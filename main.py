import discord
from discord.ext import commands
import os
import logging
import asyncio
from dotenv import load_dotenv

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()]
)
logger = logging.getLogger("swtor_bot")

# Chargement des variables d'environnement
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
PREFIX = os.getenv("COMMAND_PREFIX", "!")

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Initialisation du bot
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

@bot.event
async def on_ready():
    """Événement déclenché quand le bot est prêt"""
    logger.info(f"Bot connecté en tant que {bot.user.name}")
    
    # Synchronisation des commandes slash
    try:
        synced = await bot.tree.sync()
        logger.info(f"Commandes slash synchronisées : {len(synced)}")
    except Exception as e:
        logger.error(f"Erreur lors de la synchronisation des commandes : {e}")
        
    # Statut du bot
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.playing, 
            name="Star Wars: The Old Republic"
        )
    )
    
    print(f"{bot.user.name} est en ligne! Utilisez /swtor pour les commandes.")

@bot.event
async def on_guild_join(guild):
    """Événement déclenché quand le bot rejoint un serveur"""
    logger.info(f"Bot ajouté au serveur : {guild.name} (ID: {guild.id})")
    
    # Message de bienvenue dans le premier canal textuel accessible
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            embed = discord.Embed(
                title="Merci de m'avoir ajouté à votre serveur!",
                description="Je suis un bot Discord sur le thème de Star Wars: The Old Republic. "
                           "Utilisez `/swtor help` pour voir toutes les commandes disponibles.",
                color=0xffd700  # Couleur or (thème SWTOR)
            )
            embed.set_thumbnail(url="https://i.imgur.com/XxxxXxx.png")  # Remplacer par un logo SWTOR
            await channel.send(embed=embed)
            break

# Commande de base pour le groupe de commandes SWTOR
@bot.tree.command(name="swtor", description="Commande principale du bot SWTOR")
async def swtor_base(interaction: discord.Interaction):
    """Commande principale du bot qui affiche l'aide générale"""
    embed = discord.Embed(
        title="Bot SWTOR - Aide",
        description="Voici les commandes disponibles:",
        color=0xffd700
    )
    
    embed.add_field(
        name="Informations",
        value="`/swtor class <nom>` - Informations sur une classe\n"
              "`/swtor planet <nom>` - Informations sur une planète\n"
              "`/swtor faction <nom>` - Informations sur une faction",
        inline=False
    )
    
    embed.add_field(
        name="Divertissement",
        value="`/swtor quote` - Citation aléatoire\n"
              "`/swtor trivia` - Question de trivia sur SWTOR",
        inline=False
    )
    
    embed.add_field(
        name="Utilitaires",
        value="`/swtor events` - Événements à venir\n"
              "`/swtor status` - État des serveurs",
        inline=False
    )
    
    embed.set_footer(text="Que la Force soit avec vous!")
    
    await interaction.response.send_message(embed=embed)

async def load_extensions():
    """Charge les extensions (cogs) du bot"""
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                logger.info(f"Extension chargée: {filename}")
            except Exception as e:
                logger.error(f"Échec du chargement de l'extension {filename}: {e}")

async def main():
    """Fonction principale pour démarrer le bot"""
    async with bot:
        # Chargement des extensions
        await load_extensions()
        
        # Démarrage du bot
        await bot.start(TOKEN)

# Point d'entrée principal
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Arrêt du bot à la demande de l'utilisateur")
    except Exception as e:
        logger.error(f"Erreur fatale: {e}")
