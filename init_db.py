import sqlite3

conn = sqlite3.connect("swtor_recommandations.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS recommandations (
    faction TEXT NOT NULL,
    classe TEXT NOT NULL,
    specialisation TEXT NOT NULL,
    role TEXT NOT NULL,
    maitrise TEXT NOT NULL,
    precision TEXT NOT NULL,
    alacrite TEXT NOT NULL,
    critique TEXT NOT NULL,
    niveau_min INTEGER NOT NULL,
    conseils TEXT NOT NULL
)
""")

# Insertion de quelques exemples
builds = [
    # République
    ("Republique", "Sentinelle Jedi", "Combat", "DPS", "Maitrise 2694", "Précision 2154", "Alacrité 1600", "Critique 2000", "Priorise la précision à 110%, puis équilibre afflux/critique.", 75),
    ("Republique", "Sentinelle Jedi", "Combat", "DPS", "Maitrise 1000+", "Précision 2154", "Alacrité équilibré", "Critique 4000", "Avant le niveau 75, vise surtout à apprendre ta rotation.", 50),
    # Empire
    ("Empire", "Maraudeur Sith", "Carnage", "DPS", "Maitrise 2694", "Précision 2200", "Alacrité 1500", "Critique 2000", "Très rapide et nerveuse, idéale en groupe coordonné.", 75),
    ("Empire", "Maraudeur Sith", "Carnage", "DPS", "Maitrise 1000+", "Précision moyen", "Alacrité équilibré", "Critique 4000", "Concentre-toi sur la maîtrise des sorts avant de stuffer.", 50),
]

# Exemple d'ajout de données
cursor.execute("""
INSERT INTO recommandations VALUES (
    'République',
    'Chevalier Jedi',
    'Sentinelle - Combat',
    'DPS',
    '3600',
    '2694',
    '1213',
    '1500',
    '0',
    'Utilise le burst pour profiter des fenêtres de dégâts critiques.'
)
""")

conn.commit()
conn.close()
print("Base de données créée avec succès.")