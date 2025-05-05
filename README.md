# Bot Discord SWTOR pour Render

## 🚀 Fonctionnement

- Bot en Python avec `discord.py`
- Base de données SQLite (`swtor_recommandations.db`)
- Une fois déployé sur [Render](https://render.com), le bot peut répondre aux commandes.

## 🛠 Fichiers

- `bot.py` : code principal du bot
- `init_db.py` : initialise la base de données SQLite
- `swtor_recommandations.db` : base contenant les stats et conseils

## 🧪 Test local

```
python init_db.py
python bot.py
```

## 🌐 Variables d’environnement Render

- `DISCORD_TOKEN` : ton token de bot Discord