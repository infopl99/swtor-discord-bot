import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
import os
from dotenv import load_dotenv

class RecommandationsView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=60)
        self.bot = bot
        self.faction = None
        self.classe = None
        self.niveau = None
        self.add_item(FactionSelect(self))
    
class FactionSelect(discord.ui.Select):
    def __init__(self, view):
        options = [
            discord.SelectOption(label="République"),
            discord.SelectOption(label="Empire"),
        ]
        super().__init__(placeholder="Choisis ta faction", options=options)
        self.view = view

    async def callback(self, interaction: discord.Interaction):
        self.view.faction = self.values[0]
        await interaction.response.edit_message(content="Faction choisie ! Choisis ta classe :", view=ClasseSelectView(self.view))

class ClasseSelectView(discord.ui.View):
    def __init__(self, view):
        super().__init__(timeout=60)
        self.view = view
        self.add_item(ClasseSelect(view))

class ClasseSelect(discord.ui.Select):
    def __init__(self, view):
        self.view = view
        classes = {
            "République": ["Sentinelle Jedi", "Gardien Jedi"],
            "Empire": ["Maraudeur Sith", "Ravageur Sith"],
        }
        options = [discord.SelectOption(label=cls) for cls in classes[self.view.faction]]
        super().__init__(placeholder="Choisis ta classe avancée", options=options)

    async def callback(self, interaction: discord.Interaction):
        self.view.classe = self.values[0]
        await interaction.response.edit_message(content="Classe choisie ! Choisis ton niveau :", view=NiveauSelectView(self.view))

class NiveauSelectView(discord.ui.View):
    def __init__(self, view):
        super().__init__(timeout=60)
        self.view = view
        self.add_item(NiveauSelect(view))

class NiveauSelect(discord.ui.Select):
    def __init__(self, view):
        self.view = view
        niveaux = [50, 60, 70, 75, 80]
        options = [discord.SelectOption(label=str(n)) for n in niveaux]
        super().__init__(placeholder="Choisis ton niveau", options=options)

    async def callback(self, interaction: discord.Interaction):
        self.view.niveau = int(self.values[0])
        builds = get_recommandations(self.view.faction, self.view.classe, self.view.niveau)
        if not builds:
            msg = "Aucune recommandation trouvée pour ce niveau."
        else:
            msg = ""
            for b in builds:
                msg += f"**Spé : {b[0]}**\n🛡️ Rôle : {b[1]}\n📊 Stats : {b[2]}, {b[3]}, {b[4]}, {b[5]}\n💡 {b[6]}\n\n"
        await interaction.response.edit_message(content=msg, view=None)

def get_recommandations(faction, classe, niveau):
    conn = sqlite3.connect("swtor_recommandations.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT specialisation, role, maitrise, precision, alacrite, critique, conseils
    FROM recommandations
    WHERE faction=? AND classe_avancee=? AND niveau_min<=?
    """, (faction, classe, niveau))
    results = cursor.fetchall()
    conn.close()
    return results

# Chargement du token depuis une variable d'environnement ou un fichier .env
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    from dotenv import load_dotenv
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")
    GUILD_ID = int(os.getenv("GUILD"))

# Intégration au bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@app_commands.command(name="recommandations", description="Obtiens des conseils de stats selon ta classe et ton niveau")
async def recommandations(ctx):
    await ctx.respond("Commençons par ta faction :", view=RecommandationsView(bot))

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")

    try:
        # Syncer la commande pour le serveur explicitement
        await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print("✅ Commandes slash synchronisées dans le serveur")
    except Exception as e:
        print(f"❌ Erreur de synchronisation : {e}")

@bot.event
async def setup_hook():
    extension = f"main"
    try:
        await bot.load_extension(extension)
        print(f"✅ Extension chargée : {extension}")
    except Exception as e:
        print(f"❌ Erreur chargement {extension} : {e}")

# Lancement du bot
if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ Token Discord introuvable. Vérifie .env ou la variable d'environnement DISCORD_TOKEN.")
