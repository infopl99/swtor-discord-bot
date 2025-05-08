import discord
from discord import app_commands
from discord.ext import commands
import sqlite3

class Recommandations(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="recommandations", description="Obtiens des conseils selon ta classe et ton niveau")
    @app_commands.describe(niveau="Ton niveau actuel", classe="Classe ou spécialisation")
    async def recommandations(self, interaction: discord.Interaction, niveau: int, classe: str):
        await interaction.response.send_message(
            "Commençons par ta faction :", view=RecommandationsView(self.bot), ephemeral=True
        )

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
            discord.SelectOption(label="Republique"),
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
            "Republique": ["Sentinelle Jedi", "Gardien Jedi"],
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
                msg += f"**Spé : {b[0]}**\n🛡️ Rôle : {b[1]}\n📊 Stats : {b[2]}, {b[3]}, {b[4]}\n💡 {b[5]}\n\n"
        await interaction.response.edit_message(content=msg, view=None)

def get_recommandations(faction, classe, niveau):
    conn = sqlite3.connect("swtor_recommandations.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT specialisation, role, stat1, stat2, stat3, conseils
    FROM builds
    WHERE faction=? AND classe_avancee=? AND niveau_min<=?
    """, (faction, classe, niveau))
    results = cursor.fetchall()
    conn.close()
    return results

async def setup(bot):
    await bot.add_cog(Recommandations(bot))
