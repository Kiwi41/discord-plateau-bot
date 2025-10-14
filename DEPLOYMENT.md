# 🚀 Guide de Déploiement - Discord Bot Soirées Plateaux

Ce guide détaille le déploiement du bot sur différentes plateformes.

## 🎯 Résumé des Options

| Plateforme | Coût | Difficulté | Recommandé pour |
|------------|------|------------|-----------------|
| **NAS Synology** | ~2€/mois élec. | ⭐⭐⭐ Moyen | Auto-hébergement, contrôle total |
| **Heroku** | 7$/mois | ⭐⭐ Facile | Production stable, simplicité |

---

## 🏠 NAS Synology (Auto-hébergement)

### Prérequis
- NAS Synology avec DSM 7.0+
- Package "Container Manager" installé
- Accès SSH (optionnel)

### Méthode 1: Interface Web

1. **Container Manager** :
   ```
   Package Center → Container Manager → Install
   ```

2. **Télécharger le projet** :
   ```bash
   # Sur votre PC
   git clone https://github.com/votre-username/discord-plateau-bot.git
   # Uploader le dossier sur le NAS via File Station
   ```

3. **Configuration** :
   ```bash
   # Dans File Station, créer .env dans le dossier du bot
   DISCORD_TOKEN=votre_token_bot
   GUILD_ID=votre_guild_id
   FORUM_CHANNEL_ID=votre_forum_channel_id
   REGISTRATION_URL=votre_lien_inscription
   TIMEZONE=Europe/Paris
   ```

4. **Déploiement** :
   ```
   Container Manager → Project → Create
   → Set project folder path
   → docker-compose.yml détecté automatiquement
   → Build and run
   ```

### Méthode 2: SSH (Avancé)

```bash
# Connexion SSH au NAS
ssh admin@ip-de-votre-nas

# Navigation vers dossier Docker
cd /volume1/docker/

# Clone du projet
sudo git clone https://github.com/votre-username/discord-plateau-bot.git
cd discord-plateau-bot

# Configuration
sudo cp .env.example .env
sudo nano .env  # Éditer avec vos tokens

# Démarrage
sudo docker compose up -d

# Vérification
sudo docker compose logs -f plateau-bot
```

### Monitoring Synology

1. **Container Manager** → plateau-bot → Details
2. **Logs** : Affichage temps réel
3. **Auto-restart** : Configuré dans docker-compose.yml
4. **Ressources** : CPU/RAM monitoring

---

## ⚡ Heroku (Payant mais Stable)

### Configuration Heroku

1. **Heroku CLI** :
   ```bash
   # Installation
   curl https://cli-assets.heroku.com/install.sh | sh
   
   # Login
   heroku login
   ```

2. **Création app** :
   ```bash
   heroku create discord-plateau-bot-nom-unique
   ```

3. **Variables** :
   ```bash
   heroku config:set DISCORD_TOKEN=votre_token
   heroku config:set GUILD_ID=votre_guild_id
   heroku config:set FORUM_CHANNEL_ID=votre_forum_channel_id
   heroku config:set REGISTRATION_URL=votre_lien
   ```

4. **Déploiement** :
   ```bash
   git push heroku main
   ```

### Procfile (requis pour Heroku)

```
worker: node index.js
```

### Configuration Dynos

```bash
# Arrêter web dyno (gratuit, inutile pour un bot)
heroku ps:scale web=0

# Activer worker dyno ($7/mois)  
heroku ps:scale worker=1
```

---

## 🔧 Dépannage Commun

### Logs Docker

```bash
# Voir les logs
docker compose logs plateau-bot

# Logs en temps réel
docker compose logs -f plateau-bot

# Redémarrer
docker compose restart plateau-bot
```

### Tests de Connectivité

```bash
# Test de construction
docker build -t test-bot .

# Test d'exécution
docker run --env-file .env test-bot

# Nettoyage
docker rmi test-bot
```

### Variables d'Environnement

```bash
# Vérification locale
cat .env

# Vérification dans container
docker compose exec plateau-bot env | grep DISCORD
```

---

## 📊 Monitoring et Maintenance

### Vérifications Régulières

1. **Logs** : Vérifier absence d'erreurs
2. **Uptime** : Bot connecté 24/7
3. **Posts** : Création automatique samedis 3h
4. **Ressources** : CPU/RAM usage

### Mise à jour

```bash
# Pull nouvelles versions
git pull origin main

# Redémarrage avec nouvelle image
docker compose up -d --build
```

### Backup Configuration

```bash
# Sauvegarder .env
cp .env .env.backup

# Sauvegarder compose override si modifié
cp docker-compose.yml docker-compose.yml.backup
```

---

## ❓ FAQ Déploiement

**Q: Quelle plateforme choisir ?**
- **Auto-hébergement** : NAS Synology (~2€/mois élec.)
- **Simplicité et fiabilité** : Heroku (7$/mois, support professionnel)

**Q: Combien coûte l'hébergement ?**
- NAS Synology : ~2€/mois électricité
- Heroku : 7$/mois

**Q: Le bot fonctionne hors ligne ?**
Non, le bot nécessite une connexion internet constante pour Discord.

**Q: Puis-je héberger plusieurs bots ?**
Oui, chaque bot nécessite son propre token et container.

**Q: Consommation ressources ?**
- RAM : ~50MB en fonctionnement
- CPU : Minimal (pics lors création posts)
- Réseau : ~1MB/jour

---

*📝 Ce guide sera mis à jour selon les évolutions des plateformes de déploiement.*