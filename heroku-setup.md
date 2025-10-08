# Guide de déploiement Heroku pour le bot Discord

## 📋 Étapes de déploiement

### 1. Vérification du compte Heroku
- ✅ Heroku CLI installé
- ❌ **Compte à vérifier** : https://heroku.com/verify
- ❌ Ajouter des informations de paiement (gratuit pour les apps simples)

### 2. Création de l'application (après vérification)
```bash
# Créer l'app Heroku
heroku create discord-plateau-bot --region eu

# Ou avec un nom aléatoire si celui-ci est pris
heroku create --region eu
```

### 3. Configuration des variables d'environnement
```bash
# Définir les variables d'environnement sur Heroku
heroku config:set DISCORD_TOKEN=ton_token_discord_ici
heroku config:set GUILD_ID=ton_guild_id_ici
heroku config:set FORUM_CHANNEL_ID=ton_forum_channel_id_ici
heroku config:set REGISTRATION_URL=ton_url_inscription_ici
heroku config:set TIMEZONE=Europe/Paris
heroku config:set EVENT_ID=ton_event_id_ici
```

### 4. Déploiement
```bash
# Pousser le code vers Heroku
git push heroku master

# Démarrer l'application
heroku ps:scale worker=1

# Vérifier les logs
heroku logs --tail
```

## 🔧 Variables d'environnement requises

| Variable | Description | Obligatoire |
|----------|-------------|-------------|
| `DISCORD_TOKEN` | Token du bot Discord | ✅ |
| `GUILD_ID` | ID du serveur Discord | ✅ |
| `FORUM_CHANNEL_ID` | ID du canal forum | ✅ |
| `REGISTRATION_URL` | URL d'inscription | ✅ |
| `EVENT_ID` | ID de l'événement récurrent | ⚠️ |
| `TIMEZONE` | Fuseau horaire | ⚠️ |

## 📊 Commandes utiles après déploiement

```bash
# Voir les logs en temps réel
heroku logs --tail

# Redémarrer l'app
heroku restart

# Voir le statut
heroku ps

# Ouvrir l'app dans le navigateur (dashboard)
heroku open

# Variables d'environnement
heroku config
```

## 🎯 Prochaines étapes

1. **Vérifier le compte Heroku** sur https://heroku.com/verify
2. **Récupérer les IDs Discord** nécessaires :
   - Token du bot (Discord Developer Portal)
   - Guild ID (serveur Discord)
   - Forum Channel ID (canal forum)
   - Event ID (événement récurrent optionnel)
3. **Créer l'app et configurer les variables**
4. **Déployer et tester**

## ⚡ Configuration rapide (une fois le compte vérifié)

```bash
# Script de déploiement rapide
heroku create discord-plateau-bot --region eu
heroku config:set DISCORD_TOKEN=XXX GUILD_ID=XXX FORUM_CHANNEL_ID=XXX REGISTRATION_URL=XXX TIMEZONE=Europe/Paris
git push heroku master
heroku ps:scale worker=1
heroku logs --tail
```