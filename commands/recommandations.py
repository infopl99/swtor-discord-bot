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
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send(
            "Commençons par ta faction :",
            view=RecommandationsView(self.bot),
            ephemeral=True
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
    def __init__(self, parent_view):
        options = [
            discord.SelectOption(label="Republique"),
            discord.SelectOption(label="Empire"),
        ]
        super().__init__(placeholder="Choisis ta faction", options=options)
        self.parent_view = parent_view

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.parent_view.faction = self.values[0]
        await interaction.followup.edit_message(
            message_id=interaction.message.id,
            content="Faction choisie ! Choisis ta classe :",
            view=ClasseSelectView(self.parent_view)
        )

class ClasseSelectView(discord.ui.View):
    def __init__(self, parent_view):
        super().__init__(timeout=60)
        self.parent_view = parent_view
        self.add_item(ClasseSelect(parent_view))

class ClasseSelect(discord.ui.Select):
    def __init__(self, parent_view):
        self.parent_view = parent_view
        classes = {
            "Republique": ["Sentinelle Jedi", "Gardien Jedi"],
            "Empire": ["Maraudeur Sith", "Ravageur Sith"],
        }
        options = [discord.SelectOption(label=cls) for cls in classes[self.parent_view.faction]]
        super().__init__(placeholder="Choisis ta classe avancée", options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.parent_view.classe = self.values[0]
        await interaction.followup.edit_message(
            message_id=interaction.message.id,
            content="Classe choisie ! Choisis ton niveau :",
            view=NiveauSelectView(self.parent_view)
        )

class NiveauSelectView(discord.ui.View):
    def __init__(self, parent_view):
        super().__init__(timeout=60)
        self.parent_view = parent_view
        self.add_item(NiveauSelect(parent_view))

class NiveauSelect(discord.ui.Select):
    def __init__(self, parent_view):
        self.parent_view = parent_view
        niveaux = [50, 60, 70, 75, 80]
        options = [discord.SelectOption(label=str(n)) for n in niveaux]
        super().__init__(placeholder="Choisis ton niveau", options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.parent_view.niveau = int(self.values[0])
        builds = get_recommandations(
            self.parent_view.faction,
            self.parent_view.classe,
            self.parent_view.niveau
        )
        if not builds:
            msg = "Aucune recommandation trouvée pour ce niveau."
        else:
            msg = ""
            for b in builds:
                msg += f"**Spé : {b[0]}**\n🛡️ Rôle : {b[1]}\n📊 Stats : {b[2]}, {b[3]}, {b[4]}\n💡 {b[5]}\n\n"
        await interaction.followup.edit_message(
            message_id=interaction.message.id,
            content=msg,
            view=None
        )

def get_recommandations(faction, classe, niveau):
    conn = sqlite3.connect("swtor_recommandations.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT specialisation, role, maitrise, precision, alacrite, critique, niveau_min, conseils
    FROM recommandations
    WHERE faction=? AND classe=? AND niveau_min<=?
    """, (faction, classe, niveau))
    results = cursor.fetchall()
    conn.close()
    return results

async def setup(bot):
    await bot.add_cog(Recommandations(bot))
