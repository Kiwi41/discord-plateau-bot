# Bot Discord Python - Guide de Déploiement Docker

## 🚀 Démarrage rapide

### Option 1: Script automatique (Recommandé)

```bash
# Rendre le script exécutable
chmod +x deploy-python.sh

# Lancer le déploiement
./deploy-python.sh
```

### Option 2: Commandes manuelles

#### Build local
```bash
# Build de l'image
docker compose -f docker-compose.python.yml build

# Lancer le bot
docker compose -f docker-compose.python.yml up -d

# Voir les logs
docker compose -f docker-compose.python.yml logs -f
```

#### Image pré-construite
```bash
# Pull et lancer
docker compose -f docker-compose.prod.python.yml up -d

# Voir les logs
docker compose -f docker-compose.prod.python.yml logs -f
```

## 📋 Prérequis

1. **Docker installé** : https://docs.docker.com/get-docker/
2. **Docker Compose installé** : https://docs.docker.com/compose/install/
3. **Fichier .env configuré** avec vos tokens Discord

## ⚙️ Configuration

Créer un fichier `.env` avec :

```bash
DISCORD_TOKEN=votre_token_bot
GUILD_ID=votre_guild_id
FORUM_CHANNEL_ID=votre_forum_channel_id
REGISTRATION_URL=https://votre-lien-inscription.com
EVENT_ID=votre_event_id_optionnel
TIMEZONE=Europe/Paris
```

## 🔧 Commandes Docker utiles

### Gestion du conteneur

```bash
# Démarrer
docker compose -f docker-compose.python.yml up -d

# Arrêter
docker compose -f docker-compose.python.yml down

# Redémarrer
docker compose -f docker-compose.python.yml restart

# Status
docker compose -f docker-compose.python.yml ps
```

### Logs et debug

```bash
# Voir les logs en temps réel
docker compose -f docker-compose.python.yml logs -f

# Voir les derniers logs
docker compose -f docker-compose.python.yml logs --tail=50

# Entrer dans le conteneur
docker exec -it discord-plateau-bot-python /bin/bash
```

### Build et images

```bash
# Rebuild l'image
docker compose -f docker-compose.python.yml build --no-cache

# Lister les images
docker images | grep discord-plateau

# Supprimer l'image
docker rmi discord-plateau-bot-python
```

## 🐳 Déploiement sur différentes plateformes

### Synology NAS

1. Copier les fichiers sur le NAS :
```bash
scp bot.py requirements.txt Dockerfile.python docker-compose.python.yml .env user@nas:/volume1/docker/discord-bot/
```

2. Se connecter au NAS et lancer :
```bash
ssh user@nas
cd /volume1/docker/discord-bot
docker compose -f docker-compose.python.yml up -d
```

### Railway.app

```bash
# Installer Railway CLI
npm i -g @railway/cli

# Login
railway login

# Déployer
railway up
```

### VPS / Serveur cloud

```bash
# Cloner le repo
git clone https://github.com/votre-username/discord-plateau-bot.git
cd discord-plateau-bot

# Configurer .env
cp .env.example.python .env
nano .env

# Lancer
./deploy-python.sh
```

## 🔄 Mise à jour du bot

```bash
# Pull les dernières modifications
git pull

# Rebuild et redémarrer
docker compose -f docker-compose.python.yml up -d --build
```

## 🆘 Dépannage

### Le bot ne démarre pas

```bash
# Vérifier les logs
docker compose -f docker-compose.python.yml logs

# Vérifier les variables d'environnement
docker compose -f docker-compose.python.yml config
```

### Problème de permissions

```bash
# Le bot tourne avec l'utilisateur botuser (UID 1000)
# Vérifier les permissions des fichiers
ls -la bot.py
```

### Rebuild complet

```bash
# Tout supprimer et recommencer
docker compose -f docker-compose.python.yml down -v
docker compose -f docker-compose.python.yml build --no-cache
docker compose -f docker-compose.python.yml up -d
```

## 📊 Monitoring

### Voir l'utilisation des ressources

```bash
# Stats du conteneur
docker stats discord-plateau-bot-python
```

### Logs rotatifs

Les logs sont automatiquement limités :
- Taille max par fichier : 10 MB
- Nombre max de fichiers : 3

## 🔐 Sécurité

- ⚠️ Ne jamais commiter le fichier `.env`
- ✅ Le bot tourne avec un utilisateur non-root
- ✅ Fichiers montés en lecture seule (`:ro`)
- ✅ Restart automatique en cas de crash

## 📦 Structure des fichiers

```
.
├── bot.py                          # Code du bot
├── requirements.txt                # Dépendances Python
├── Dockerfile.python              # Configuration Docker
├── docker-compose.python.yml      # Compose pour build local
├── docker-compose.prod.python.yml # Compose pour image registry
├── deploy-python.sh               # Script de déploiement
└── .env                           # Variables d'environnement (ne pas commiter!)
```
