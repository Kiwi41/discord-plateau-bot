#!/bin/bash

echo "🔄 Remplacement des diagrammes SVG par des descriptions textuelles GitHub-friendly"
echo

# Créer un nouveau README sans les SVG problématiques
cat > "/home/a154355/git/perso/Discord/docs/README.md" << 'EOF'
# 🎲 Bot Discord pour Soirées Plateaux - Documentation Complète

## 📋 Table des matières

1. [Introduction](#introduction)
2. [Qu'est-ce que ce bot ?](#quest-ce-que-ce-bot)
3. [Comment ça fonctionne ?](#comment-ça-fonctionne)
4. [Architecture du système](#architecture-du-système)
5. [Installation et configuration](#installation-et-configuration)
6. [Utilisation](#utilisation)
7. [Dépannage](#dépannage)
8. [Maintenance](#maintenance)

---

## 🎯 Introduction

Ce bot Discord a été créé pour **automatiser la gestion des soirées plateaux** dans votre serveur Discord. Il crée automatiquement des posts dans un forum pour planifier les soirées jeux de plateau du vendredi soir.

### 🎪 Pour qui ?

- **Communautés de jeux de plateau** 
- **Serveurs Discord** organisant des événements récurrents
- **Gestionnaires de communautés** voulant automatiser la planification

---

## 🤖 Qu'est-ce que ce bot ?

### Fonctionnalités principales

✅ **Création automatique de posts** chaque mardi à 10h  
✅ **Récupération d'informations** depuis les événements Discord  
✅ **Gestion intelligente des doublons** (pas de posts multiples)  
✅ **Mise à jour automatique** si les infos changent  
✅ **Commandes manuelles** pour créer ou traiter les posts  
✅ **Support des fuseaux horaires**  

### Ce que fait le bot concrètement

1. **Chaque mardi à 10h** → Crée des posts pour les 4 prochains vendredis
2. **Récupère les infos** → Heure, lieu, description depuis Discord
3. **Poste dans le forum** → Message avec toutes les infos importantes
4. **Met à jour** → Si tu changes l'événement, le post se met à jour

---

## 🔄 Comment ça fonctionne ?

### Le cycle de vie du bot

```
🕙 Mardi 10h00
    ↓
🔍 Recherche événements Discord
    ↓
📅 Filtre les 4 prochains vendredis
    ↓
📝 Crée/met à jour les posts forum
    ↓
✅ Marque comme traités
    ↓
😴 Attend le prochain mardi
```

### Architecture du système

```
┌─────────────────────────────────────────┐
│              🎮 Discord                 │
├─────────────────────────────────────────┤
│  📅 Événements  │  💬 Forum Planning   │
│  "Soirée Plateau│  Posts automatiques   │
│   Vendredi"     │  avec infos détaillées│
└─────────────┬───┴──────────▲────────────┘
              │              │
              │ Lit          │ Écrit
              ▼              │
┌─────────────────────────────────────────┐
│            ☁️ Heroku Cloud              │
├─────────────────────────────────────────┤
│           🤖 Bot Discord                │
│  ┌─────────────────────────────────────┐│
│  │     📋 Processus Principal         ││
│  │                                    ││
│  │  • Cron: Mardi 10h                ││
│  │  • Fetch événements Discord       ││
│  │  • Traite 4 prochains vendredis   ││
│  │  • Crée posts forum               ││
│  │  • Évite les doublons             ││
│  │                                    ││
│  └─────────────────────────────────────┘│
│                                         │
│  💾 Variables d'environnement:          │
│     DISCORD_TOKEN, GUILD_ID, etc.      │
└─────────────────────────────────────────┘
```

### Flux de données

```
Événement Discord → Bot → Post Forum

┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  📅 Événement   │    │   🤖 Bot         │    │  💬 Post Forum  │
│                 │────▶                  │────▶                 │
│ • Nom          │    │ • Lit événement   │    │ • Titre         │
│ • Date         │    │ • Extrait infos   │    │ • Description   │
│ • Heure        │    │ • Format message  │    │ • Lieu          │
│ • Lieu         │    │ • Évite doublons  │    │ • Heure         │
│ • Description  │    │ • Crée/met à jour│    │ • Lien Discord  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

---

## 🏗️ Architecture du système

### Composants principaux

#### 1. 🤖 **Bot Discord** (Node.js)
- **Fichier principal :** `index.js`
- **Framework :** discord.js v14
- **Planification :** node-cron
- **Hébergement :** Heroku (dyno worker)

#### 2. 🎮 **Discord Server**
- **Événements :** Source de données
- **Forum :** Destination des posts
- **Permissions :** Bot avec accès lecture/écriture

#### 3. ☁️ **Heroku Cloud**
- **Type :** Worker dyno (background process)
- **Région :** Europe
- **Variables :** Configuration sécurisée

### Workflow utilisateur

```
👤 Utilisateur Discord
    │
    │ 1. Crée un événement "Soirée Plateau Vendredi"
    ▼
📅 Événement Discord
    │
    │ 2. Bot détecte automatiquement (mardi 10h)
    ▼
🤖 Bot Processing
    │
    │ 3. Extrait les informations
    │ 4. Vérifie pas de doublon
    │ 5. Formate le message
    ▼
💬 Post Forum
    │
    │ 6. Utilisateurs voient le post
    ▼
👥 Communauté informée
```

---

## ⚙️ Installation et configuration

### 🚀 Installation rapide (Débutants)

👉 **[Guide d'installation simplifié](QUICK_INSTALL.md)**

### 🔧 Installation complète

#### Prérequis

- **Node.js** version 18.0.0 ou supérieure
- **Compte Discord Developer** (pour créer le bot)
- **Serveur Discord** avec permissions administrateur
- **Compte Heroku** (pour l'hébergement)

#### Étape 1 : Configuration Discord

1. **Créer une application Discord**
   - Va sur [Discord Developer Portal](https://discord.com/developers/applications)
   - Clique "New Application"
   - Nomme ton bot (ex: "Bot Soirées Plateaux")

2. **Créer le bot**
   - Onglet "Bot" → "Add Bot"
   - Note le **Token** (garde-le secret !)
   - Active "Message Content Intent"

3. **Inviter le bot sur ton serveur**
   - Onglet "OAuth2" → "URL Generator"
   - Coches : `bot`, `applications.commands`
   - Permissions : `Send Messages`, `Create Forum Posts`, `View Channels`
   - Utilise l'URL générée pour inviter le bot

#### Étape 2 : Récupérer les IDs Discord

```javascript
// Active le mode développeur Discord
// Paramètres → Avancés → Mode développeur

// Clique droit sur ton serveur → "Copier l'ID"
GUILD_ID = "ton_guild_id"

// Clique droit sur le canal forum → "Copier l'ID"  
FORUM_CHANNEL_ID = "ton_forum_channel_id"
```

#### Étape 3 : Configuration locale

1. **Clone le projet**
```bash
git clone https://github.com/Kiwi41/discord-plateau-bot.git
cd discord-plateau-bot
```

2. **Installe les dépendances**
```bash
npm install
```

3. **Configure les variables (.env)**
```bash
cp .env.example .env
# Édite .env avec tes valeurs
```

4. **Test local**
```bash
node index.js
```

#### Étape 4 : Déploiement Heroku

1. **Installe Heroku CLI**
```bash
# Ubuntu/Debian
curl https://cli-assets.heroku.com/install.sh | sh
```

2. **Login et création app**
```bash
heroku login
heroku create discord-plateau-bot-TONNOM
```

3. **Configuration variables**
```bash
heroku config:set DISCORD_TOKEN="ton_token"
heroku config:set GUILD_ID="ton_guild_id"
heroku config:set FORUM_CHANNEL_ID="ton_forum_id"
# ... autres variables
```

4. **Déploiement**
```bash
git add .
git commit -m "Initial deployment"
git push heroku main
```

5. **Activation**
```bash
heroku ps:scale worker=1
```

### 📋 Variables d'environnement

| Variable | Description | Exemple |
|----------|-------------|---------|
| `DISCORD_TOKEN` | Token du bot Discord | `MTIzNDU2Nzg5...` |
| `GUILD_ID` | ID du serveur Discord | `987654321012345678` |
| `FORUM_CHANNEL_ID` | ID du canal forum | `123456789012345678` |
| `SIGNUP_URL` | Lien d'inscription | `https://forms.gle/...` |
| `TZ` | Fuseau horaire | `Europe/Paris` |

---

## 🎮 Utilisation

### Fonctionnement automatique

Le bot fonctionne **automatiquement** :
- **Chaque mardi à 10h** (fuseau configuré)
- Cherche les événements "Soirée Plateau" des 4 prochains vendredis
- Crée des posts dans le forum avec toutes les infos

### Commandes manuelles

#### `/create-plateau-post`
Crée manuellement un post pour un vendredi spécifique

**Usage :**
```
/create-plateau-post date:2024-03-15
```

#### `/process-one-friday`  
Traite un vendredi spécifique (recherche événement + crée post)

**Usage :**
```
/process-one-friday date:2024-03-15
```

### Exemple de post créé

```markdown
# 🎲 Soirée Plateau - Vendredi 15 Mars 2024

📅 **Date :** Vendredi 15 Mars 2024
🕖 **Heure :** 19h30 - 23h00  
📍 **Lieu :** Bar "Les Dés Pipés", 42 rue du Jeu, Lyon
📝 **Description :** 
Venez nombreux pour une soirée conviviale autour de jeux de plateau !
Au programme : nouveautés, classiques et découvertes.

🎯 **Inscription :** https://forms.gle/abc123def456

💬 **Questions ?** Ping @OrganisateurJeux
```

---

## 🔧 Dépannage

### Problèmes courants

#### 🚫 Le bot ne crée pas de posts

**Vérifications :**
1. **Bot en ligne ?** `heroku ps` → doit montrer `worker.1: up`
2. **Permissions Discord ?** Le bot peut écrire dans le forum ?
3. **Variables environnement ?** `heroku config` → vérifier toutes les vars
4. **Logs d'erreur ?** `heroku logs --tail`

**Solutions :**
```bash
# Redémarre le bot
heroku ps:restart worker

# Vérifie les logs en temps réel  
heroku logs --tail

# Teste une commande manuelle
/create-plateau-post date:2024-03-15
```

#### 🔄 Posts créés en double

**Cause :** Mécanisme anti-doublon défaillant

**Solution :**
```bash
# Vérifie les logs pour comprendre
heroku logs --grep "already exists"

# Supprime manuellement les doublons sur Discord
# Le bot se resynchronisera au prochain cycle
```

#### 📅 Mauvais événements détectés

**Cause :** Filtre de nom d'événement trop strict/large

**Solution :**
```javascript
// Modifier dans index.js la fonction de filtre
const plateauEvents = events.filter(event => 
    event.name.toLowerCase().includes('plateau') &&
    event.name.toLowerCase().includes('vendredi')
);
```

#### 🕐 Problème de fuseau horaire

**Vérification :**
```bash
heroku config:get TZ
# Doit retourner: Europe/Paris (ou ton fuseau)
```

**Correction :**
```bash
heroku config:set TZ=Europe/Paris
heroku ps:restart worker
```

### Logs utiles

#### Surveiller l'activité
```bash
# Logs en temps réel
heroku logs --tail

# Logs des dernières 24h
heroku logs --since="1 day ago"

# Chercher des erreurs
heroku logs --grep="ERROR"
```

#### Informations système
```bash
# Statut des processus
heroku ps

# Variables d'environnement
heroku config

# Utilisation ressources
heroku ps:type
```

---

## 🔄 Maintenance

### Surveillance recommandée

#### Contrôles hebdomadaires
- [ ] **Posts créés** : Vérifier que les posts apparaissent chaque mardi
- [ ] **Contenu posts** : Infos cohérentes avec événements Discord
- [ ] **Logs** : Pas d'erreurs récurrentes

#### Contrôles mensuels
- [ ] **Usage Heroku** : Vérifier les quotas dyno
- [ ] **Token Discord** : Renouveler si nécessaire
- [ ] **Mise à jour code** : Nouvelles versions disponibles

### Mise à jour du bot

#### Mise à jour mineure (correction bugs)
```bash
git pull origin main
git push heroku main
heroku ps:restart worker
```

#### Mise à jour majeure (nouvelles fonctionnalités)
```bash
# Test en local d'abord
npm test
node index.js

# Si OK, déploie
git push heroku main
heroku ps:restart worker

# Surveille les logs
heroku logs --tail
```

### Sauvegarde et restauration

#### Sauvegarde configuration
```bash
# Exporte toutes les variables
heroku config --json > backup-config.json

# Exporte les logs récents
heroku logs --num=1500 > backup-logs.txt
```

#### Restauration après problème
```bash
# Rollback vers version précédente
heroku releases:rollback

# Re-configure les variables si nécessaire
heroku config:set DISCORD_TOKEN="..."

# Redémarre
heroku ps:restart worker
```

---

## 📚 Ressources supplémentaires

### Documentation technique
- **[FAQ - Questions fréquentes](FAQ.md)**
- **[Guide installation rapide](QUICK_INSTALL.md)**
- **[Fichier de synthèse](SYNTHESIS.md)**

### Liens utiles
- **Discord.js :** https://discord.js.org/
- **Heroku :** https://devcenter.heroku.com/
- **Node-cron :** https://github.com/kelektiv/node-cron

### Support
- **Issues GitHub :** [Créer un ticket](https://github.com/Kiwi41/discord-plateau-bot/issues)
- **Discord Communauté :** Ping @OrganisateurJeux

---

## 🎯 Synthèse pour développeurs

**Technologies :** Node.js, discord.js v14, node-cron, Heroku  
**Pattern :** Event-driven automation avec anti-doublon  
**Déploiement :** Worker dyno Heroku avec variables d'environnement  
**Monitoring :** Logs Heroku + Discord embed status  

**Points clés :**
- Authentification Discord via token bot
- Récurrence cron : `0 10 * * 2` (mardi 10h)  
- Anti-doublon via nom + date dans titre post
- Retry logic avec backoff exponentiel
- Support multi-timezone via process.env.TZ

EOF

echo "✅ README mis à jour sans SVG problématiques"
echo "🔄 Les diagrammes sont maintenant en ASCII art GitHub-friendly"