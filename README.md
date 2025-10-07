# Disc### ✨ **Automatisation avancée**
- 📅 **Traitement des 4 prochains vendredis** : Plus pratique et réactif qu'un mois entier
- 🔄 **Mise à jour intelligente** : Détecte et met à jour automatiquement les changements
- ⏰ **Planification flexible** : Samedis à 3h00 du matin (configurable)
- 🛡️ **Protection anti-doublon** : Évite les posts en doubleot pour Soirées Plateaux 🎲

Bot Discord intelligent qui crée et met à jour automatiquement des posts dans un forum pour planifier les soirées plateaux du vendredi soir.

## 🚀 Fonctionnalités

### ✨ **Automatisation avancée**
- ✅ **Traitement mensuel** : Crée tous les posts du mois suivant en une fois
- 🔄 **Mise à jour intelligente** : Détecte et met à jour automatiquement les changements
- 📅 **Planification flexible** : Samedis à 3h00 du matin (configurable)
- �️ **Protection anti-doublon** : Évite les posts en double

### 🎯 **Récupération d'informations automatique**
- 📅 **Date et heure** : Extraites directement depuis les événements Discord
- 📍 **Lieu intelligent** : Support des lieux physiques, salons vocaux et scènes
- 🔗 **Liens Google Maps** : Formatage automatique avec liens cliquables
- 📝 **Description dynamique** : Utilise la description de l'événement Discord

### 🎨 **Interface utilisateur**
- 💎 **Messages élégants** : Embeds Discord avec mise en forme soignée
- 🌍 **Support des fuseaux horaires** : Affichage correct selon votre région
- � **Liens directs** : Vers l'événement Discord spécifique ou récurrent

## 📋 Prérequis

1. **Node.js** (version 18 ou supérieure)
   - Télécharger depuis [nodejs.org](https://nodejs.org/)
   - Vérifier l'installation avec `node --version`

2. **Bot Discord configuré**
   - Créer une application sur [Discord Developer Portal](https://discord.com/developers/applications)
   - Créer un bot et récupérer le token
   - Inviter le bot sur votre serveur avec les permissions nécessaires

## 🛠️ Installation

### 1. Cloner et installer les dépendances

```bash
# Naviguer dans le dossier du projet
cd "C:\Users\a154355\OneDrive - Worldline SA\Dev\Discord"

# Installer les dépendances
npm install
```

### 2. Configuration des variables d'environnement

1. Copier le fichier d'exemple:
   ```bash
   copy .env.example .env
   ```

2. Modifier le fichier `.env` avec vos valeurs:
   ```env
   DISCORD_TOKEN=votre_token_bot_discord
   GUILD_ID=id_de_votre_serveur
   FORUM_CHANNEL_ID=id_du_canal_forum_planning_plateau
   REGISTRATION_URL=https://votre-lien-inscription.com
   TIMEZONE=Europe/Paris
   ```

### 3. Obtenir les IDs Discord

#### Token du bot:
1. Aller sur [Discord Developer Portal](https://discord.com/developers/applications)
2. Sélectionner votre application → Bot → Token

#### Guild ID (ID du serveur):
1. Activer le mode développeur dans Discord (Paramètres utilisateur → Avancé → Mode développeur)
2. Clic droit sur votre serveur → Copier l'ID

#### Forum Channel ID:
1. Clic droit sur le canal forum "planning-plateau" → Copier l'ID

## 🚀 Utilisation

### Démarrer le bot
```bash
npm start
```

### Mode développement (rechargement automatique)
```bash
npm run dev
```

### Commandes VS Code
- **Ctrl+Shift+P** → "Tasks: Run Task" → "Install Dependencies"
- **Ctrl+Shift+P** → "Tasks: Run Task" → "Start Bot"

## 📅 Planification Automatique

Le bot traite automatiquement **tous les samedis à 3h00** du matin :
- � **Traitement des 4 prochains vendredis** : Plus pratique qu'un mois entier
- 🔄 **Mise à jour intelligente** : Met à jour les posts existants si les informations changent
- 🎯 **Détection automatique** : Trouve les événements Discord correspondant à chaque date

### 👑 Commandes Administrateur

Les administrateurs peuvent utiliser ces commandes dans le chat :

| Commande | Description |
|----------|-------------|
| `!create-plateau-post` | Crée ou met à jour le post pour le prochain vendredi uniquement |
| `!process-next-month` | Traite les 4 prochains vendredis (création + mise à jour) |
| `!plateau-help` | Affiche l'aide des commandes disponibles |

### ⚙️ Modifier la planification

Pour changer l'heure/jour de planification, modifiez cette ligne dans `index.js` :
```javascript
// Samedi 3h00 du matin (format cron: minute heure * * jour_semaine)
cron.schedule('0 3 * * 6', () => { ... });

// Exemples d'autres planifications :
// Lundi 9h00    : '0 9 * * 1'
// Mercredi 15h30 : '30 15 * * 3'  
// Vendredi 8h45  : '45 8 * * 5'
```

## 🧠 Fonctionnement Intelligent

### 📅 **Traitement des 4 Prochains Vendredis (Samedi 3h00)**

#### 🎯 **Pourquoi 4 vendredis plutôt qu'un mois entier ?**
- ✅ **Plus réactif** : Couvre toujours environ 1 mois glissant
- ✅ **Plus logique** : Pas de coupure artificielle en fin de mois
- ✅ **Plus pratique** : Traite exactement ce qui est nécessaire
- ✅ **Plus prévisible** : Toujours 4 dates, peu importe le mois

#### 🔄 **Processus de traitement :**
1. **🗓️ Calcul** → Détermine les 4 prochains vendredis à partir de maintenant
2. **🔍 Recherche** → Trouve les événements Discord correspondant à chaque date
3. **⚡ Traitement séquentiel** → Pour chaque vendredi :
   - 🆕 **Nouveau post** → Crée avec les informations de l'événement
   - 🔄 **Post existant** → Compare et met à jour si nécessaire  
   - ✅ **Déjà à jour** → Laisse inchangé
4. **📊 Résumé** → Statistiques détaillées (créés, mis à jour, inchangés, erreurs)

### 🎲 **Logique de Récupération Intelligente**
| Priorité | Source | Comportement |
|----------|--------|--------------|
| 🏆 **1** | Événement spécifique trouvé | Utilise toutes les informations exactes |
| 📅 **2** | Événement récurrent configuré | Adapte date, utilise heure/lieu de référence |
| 🔗 **3** | URL de fallback | Valeurs par défaut (19h00, lieu à définir) |

### 🔄 **Système de Mise à Jour Avancé**
- ✅ **Détection précise** : Compare heure, lieu, description
- 🎯 **Mise à jour ciblée** : Modifie uniquement ce qui a changé  
- 📝 **Logs explicites** : Indique exactement les changements effectués
- 🛡️ **Sécurité** : Ne touche que les messages du bot lui-même

## 🎨 Exemple de post généré

Le bot crée des posts riches avec toutes les informations extraites automatiquement :

```
🎲 Soirée Plateaux du Vendredi ! 🎲

Rejoignez-nous pour une soirée jeux de plateau conviviale !

📅 Date: vendredi 10 octobre 2025
🕖 Heure: 20:30  
📍 Lieu: 📍 [Le Cube en Bois](https://maps.google.com/...)
🎯 Événement Discord: [Rejoindre l'événement](https://discord.com/events/...)
```

### 🎯 **Adaptabilité intelligente :**
- **Événement spécifique trouvé** → Utilise ses informations exactes
- **Événement récurrent configuré** → Utilise ses paramètres par défaut  
- **Aucun événement** → Utilise l'URL d'inscription de fallback

### 📍 **Types de lieux supportés :**
- **🏢 Lieux physiques** : Affichage avec liens Google Maps cliquables
- **🔊 Salons vocaux** : Indication du salon Discord
- **🎪 Scènes Discord** : Pour les événements sur scène
- **⚙️ Personnalisé** : Tout texte configuré dans l'événement

## 🔧 Permissions Discord Requises

Le bot nécessite les permissions Discord suivantes:

### Permissions essentielles
- ✅ `Send Messages` - Envoyer des messages
- ✅ `Create Public Threads` - Créer des posts dans le forum  
- ✅ `Send Messages in Threads` - Poster dans les threads du forum
- ✅ `Embed Links` - Créer des embeds riches
- ✅ `Read Message History` - Lire l'historique pour les mises à jour

### Permissions pour les événements
- ✅ `View Guild Events` - Lire les événements du serveur
- ✅ `Manage Events` - Accéder aux détails des événements (optionnel)

### Invitation du bot
Utilisez ce template d'URL d'invitation (remplacez `YOUR_BOT_ID`) :
```
https://discord.com/api/oauth2/authorize?client_id=YOUR_BOT_ID&permissions=515396344896&scope=bot
```

## 📂 Structure du projet

```
Discord/
├── index.js                    # 🤖 Bot principal avec toutes les fonctionnalités
├── config.js                   # ⚙️ Classe de gestion de la configuration  
├── package.json                # 📦 Dépendances et scripts npm
├── .env.example               # 📋 Modèle de configuration
├── .env                       # 🔐 Configuration (à créer)
├── .gitignore                 # 🚫 Fichiers ignorés par git
├── README.md                  # 📖 Ce fichier de documentation
└── .github/
    └── copilot-instructions.md # 🛠️ Instructions pour GitHub Copilot
```

### 🧠 **Fonctions principales dans `index.js` :**

| Fonction | Description |
|----------|-------------|
| `getNextFriday()` | 📅 Calcule le prochain vendredi |
| `getNextFourFridays()` | � Obtient les 4 prochains vendredis |
| `findFridayEvent()` | 🔍 Cherche l'événement Discord correspondant |
| `processOneFriday()` | 🎯 Traite un vendredi (création/mise à jour) |
| `processNextFourFridays()` | 📊 Traite les 4 prochains vendredis |
| `updateExistingPost()` | 🔄 Met à jour un post existant |
| `checkForDuplicates()` | 🛡️ Vérifie les doublons |

## 🐛 Dépannage

### 🚫 Le bot ne se connecte pas
- ✅ Vérifiez que le `DISCORD_TOKEN` est correct dans le fichier `.env`
- ✅ Assurez-vous que le bot est invité sur le serveur avec les bonnes permissions
- ✅ Vérifiez que le token n'a pas expiré (régénérez-le si nécessaire)

### 📝 Les posts ne se créent pas
- ✅ Vérifiez que `FORUM_CHANNEL_ID` correspond bien à votre canal forum
- ✅ Assurez-vous que le bot a les permissions pour créer des threads
- ✅ Vérifiez que le canal est bien de type "Forum" et non "Texte"
- ✅ Consultez les logs dans la console pour les erreurs détaillées

### 📅 Les informations d'événement sont incorrectes
- ✅ Vérifiez que votre `EVENT_ID` est correct (événement récurrent)
- ✅ Assurez-vous que l'événement Discord contient les bonnes informations
- ✅ Activez les logs de debug temporairement pour diagnostiquer
- ✅ Vérifiez le timezone configuré dans `.env`

### ❌ Erreur "npm command not found"
- ✅ Installez Node.js depuis [nodejs.org](https://nodejs.org/)  
- ✅ Redémarrez votre terminal après l'installation
- ✅ Vérifiez avec `node --version` et `npm --version`

### 🔄 Les mises à jour ne fonctionnent pas
- ✅ Vérifiez que le bot a la permission `Read Message History`
- ✅ Assurez-vous que les messages à mettre à jour ont bien été créés par le bot
- ✅ Consultez les logs pour voir les comparaisons effectuées

### 📊 Logs et Diagnostic

Pour activer le debug détaillé, décommentez ces lignes dans `index.js` :
```javascript
// Debug: affichage des informations de l'événement
console.log(`🔍 Debug événement trouvé:`);
console.log(`   Nom: ${fridayEvent.name}`);
// ... autres logs de debug
```

## 🔮 Évolutions Futures

### 🚀 **Fonctionnalités envisagées :**
- 📊 **Dashboard web** : Interface de gestion via navigateur
- 🔔 **Notifications** : Rappels automatiques avant les événements  
- 📈 **Statistiques** : Suivi de la participation aux événements
- 🎯 **IA** : Suggestions automatiques de jeux selon les participants
- 🌐 **Multi-serveurs** : Support de plusieurs serveurs Discord

### ⚡ **Optimisations possibles :**
- 🗄️ **Base de données** : Stockage des historiques et préférences
- 🔄 **Webhooks** : Intégration avec d'autres services (Calendrier, etc.)
- 🎨 **Templates** : Messages personnalisables selon les événements

## 🤝 Contribution et Support

### 💡 **Personnalisation**
Ce bot est conçu pour être facilement adaptable :
- 🎯 Modifiez les messages dans les `EmbedBuilder`
- 📅 Changez la planification dans `cron.schedule`  
- 🔍 Adaptez la recherche d'événements dans `findFridayEvent`
- 🎨 Personnalisez les couleurs, émojis et textes

### 🆘 **Support**
- 📖 Consultez ce README pour la configuration
- 🔧 Activez les logs de debug pour diagnostiquer
- 🤖 Utilisez les commandes `!plateau-help` pour tester
- 📝 Vérifiez les permissions Discord requises

### 🌟 **Améliorations suggérées**
N'hésitez pas à adapter le bot selon vos besoins spécifiques :
- Ajouter d'autres types d'événements (soirées jeux vidéo, etc.)
- Intégrer avec d'autres bots ou services
- Personnaliser les messages selon votre communauté

## 📄 Licence

**MIT License** - Utilisez, modifiez et distribuez librement selon vos besoins.

---

<div align="center">

**🎲 Bot Soirées Plateaux - Automatisation intelligente pour votre communauté Discord 🎲**

*Développé avec ❤️ pour simplifier l'organisation de vos soirées jeux*

</div>