# 🎲 Discord Bot pour Soirées Plateaux - Version Python

Bot Discord automatisé qui crée des posts hebdomadaires dans un forum pour planifier les soirées jeux de plateau du vendredi soir.

## 🎯 Vue d'ensemble

```mermaid
graph LR
    A[⏰ Samedi 3h00] --> B{Bot Active}
    B -->|Calcul| C[📅 Prochain Vendredi]
    C --> D{Post existe?}
    D -->|Non| E[✨ Créer Post Forum]
    D -->|Oui| F[🔄 Mettre à jour]
    E --> G[🔗 Lier Événement Discord]
    F --> G
    G --> H[📢 Post publié]
    
    style A fill:#966600,stroke:#bb7700,stroke-width:2px,color:#fff
    style B fill:#0969da,stroke:#1f6feb,stroke-width:2px,color:#fff
    style C fill:#161b22,stroke:#1f6feb,stroke-width:2px,color:#fff
    style D fill:#966600,stroke:#bb7700,stroke-width:2px,color:#fff
    style E fill:#1a7f37,stroke:#2ea043,stroke-width:2px,color:#fff
    style F fill:#966600,stroke:#bb7700,stroke-width:2px,color:#fff
    style G fill:#161b22,stroke:#1f6feb,stroke-width:2px,color:#fff
    style H fill:#1a7f37,stroke:#2ea043,stroke-width:2px,color:#fff
```

## ✨ Fonctionnalités

- **📅 Création automatique** : Posts hebdomadaires chaque samedi à 3h00
- **🎯 Intégration forum** : Utilise les forums Discord natifs
- **🎉 Création automatique d'événements** : Crée des événements Discord individuels si aucun n'existe
- **🔗 Liens automatiques** : Vers les événements Discord et inscription
- **👥 Suivi des participant·e·s** : Mise à jour automatique des inscriptions toutes les 15 minutes
- **⚡ Commandes manuelles** : Création manuelle et gestion avancée (y compris traitement de vendredis spécifiques)
- **🐳 Docker** : Déploiement conteneurisé sur NAS, cloud ou local
- **🐍 Python 3.11+** : Code moderne et maintenable
- **♾️ Écriture inclusive** : Logs et messages avec termes épicènes (participant·e·s)

## 🚀 Installation Rapide

```mermaid
flowchart TD
    START([🚀 Démarrage]) --> CHOICE{Méthode?}
    
    CHOICE -->|Docker| D1[📥 Télécharger image<br/>ghcr.io/kiwi41/discord-plateau-bot]
    CHOICE -->|Local| L1[🐍 Installer Python 3.11+]
    
    D1 --> D2[📝 Créer .env]
    L1 --> L2[📦 pip install -r requirements.txt]
    L2 --> D2
    
    D2 --> D3{Tokens OK?}
    D3 -->|Non| D2
    D3 -->|Oui| D4[▶️ Lancer Bot]
    
    D4 --> SUCCESS([✅ Bot Running])
    
    style START fill:#1a7f37,stroke:#2ea043,stroke-width:2px,color:#fff
    style CHOICE fill:#0969da,stroke:#1f6feb,stroke-width:2px,color:#fff
    style D1 fill:#161b22,stroke:#1f6feb,stroke-width:2px,color:#fff
    style L1 fill:#161b22,stroke:#1f6feb,stroke-width:2px,color:#fff
    style D2 fill:#d73a49,stroke:#f85149,stroke-width:2px,color:#fff
    style L2 fill:#161b22,stroke:#1f6feb,stroke-width:2px,color:#fff
    style D3 fill:#966600,stroke:#bb7700,stroke-width:2px,color:#fff
    style D4 fill:#161b22,stroke:#1f6feb,stroke-width:2px,color:#fff
    style SUCCESS fill:#1a7f37,stroke:#2ea043,stroke-width:2px,color:#fff
```

### Option 1: Docker (Recommandé)

```bash
# Configurer l'environnement
cp .env.example.python .env
# Éditer .env avec vos tokens Discord

# Lancer avec Docker
docker compose -f docker-compose.python.yml up -d

# Voir les logs
docker compose -f docker-compose.python.yml logs -f
```

### Option 2: Python local

```bash
# Installer Python 3.11+ et pip

# Installer les dépendances
pip install -r requirements.txt

# Configurer l'environnement
cp .env.example.python .env
# Éditer .env avec vos tokens Discord

# Démarrer le bot
python bot.py
```

## ⚙️ Configuration

### Variables d'environnement requises

Créer un fichier `.env` avec les valeurs suivantes :

```bash
DISCORD_TOKEN=votre_token_bot
GUILD_ID=votre_guild_id
FORUM_CHANNEL_ID=votre_forum_channel_id
REGISTRATION_URL=https://votre-lien-inscription.com
EVENT_ID=                        # Optionnel - Déprécié (événements créés automatiquement)
EVENT_DESCRIPTION=🎲 Soirée Plateaux du Vendredi ! 🎲\nTu aimes les jeux...  # Description des événements créés automatiquement
EVENT_LOCATION=Le Cube en Bois – https://www.google.com/maps/...              # Lieu des événements avec URL Google Maps
TIMEZONE=Europe/Paris
DRY_RUN=false                    # Mode test (true) pour voir les actions sans modifier Discord
AUTO_PROCESS=false               # Traitement automatique au démarrage (false recommandé)
```

### Variables importantes

- **EVENT_DESCRIPTION** : Texte de description pour les événements créés automatiquement (utiliser `\n` pour les sauts de ligne)
- **EVENT_LOCATION** : Lieu avec format `Nom – URL Google Maps` pour les événements externes
- **EVENT_ID** : **Déprécié** - Le bot crée maintenant des événements individuels automatiquement
- **DRY_RUN** : `true` pour tester sans modifier Discord, `false` pour production
- **AUTO_PROCESS** : `true` pour traiter automatiquement les 4 vendredis au démarrage

### 🔑 Obtenir les tokens Discord

1. **Token Bot** : [Discord Developer Portal](https://discord.com/developers/applications)
   - Créer une application → Bot → Copy Token
   
2. **Guild ID** : Clic droit sur votre serveur → "Copier l'identifiant"

3. **Forum Channel ID** : Clic droit sur votre canal forum → "Copier l'identifiant"

4. **Permissions du Bot** : Le bot nécessite les permissions suivantes :
   - ✅ Send Messages
   - ✅ Create Public Threads
   - ✅ Send Messages in Threads
   - ✅ **Manage Events** (pour créer automatiquement les événements)
   - ✅ Read Message History
   - ✅ View Channels

### 🎉 Création Automatique d'Événements

**Nouveauté** : Le bot crée maintenant automatiquement des événements Discord individuels pour chaque vendredi si aucun événement n'existe.

**Configuration** :
- **EVENT_DESCRIPTION** : Le texte de description de l'événement (utiliser `\n` pour les sauts de ligne)
- **EVENT_LOCATION** : Lieu au format `Nom – URL Google Maps`
- Les événements sont créés avec :
  - 📅 Date : Le vendredi ciblé
  - 🕖 Heure : 20:30 - 00:30 (4 heures)
  - 📍 Type : Événement externe
  - 📝 Description personnalisée depuis EVENT_DESCRIPTION

**Avantages** :
- ✅ Plus besoin d'événement récurrent
- ✅ Suivi précis des inscriptions par soirée
- ✅ Description personnalisée pour chaque événement
- ✅ Création automatique si l'événement n'existe pas

### 📅 Détection et Création des Événements Discord

Le bot détecte automatiquement les événements Discord existants et **crée automatiquement** de nouveaux événements si aucun n'est trouvé.

**Processus** :
1. 🔍 Le bot recherche un événement Discord pour le vendredi ciblé
2. ✨ Si aucun événement n'existe → **Création automatique** d'un nouvel événement
3. 🔗 Si un événement existe → Utilisation de cet événement
4. 📝 Le post du forum est lié à l'événement (existant ou créé)

**Critères de détection des événements existants** :
1. ✅ **Date** : L'événement doit être programmé le vendredi ciblé
2. ✅ **Nom** : Doit contenir l'un de ces mots-clés (insensible à la casse) :
   - `plateau`
   - `soirée` (ou `soiree`)
   - `jeu`
   - `board`
   - `game`

**Exemples de noms valides** :
- ✅ "Soirée Plateaux"
- ✅ "Jeux de plateau"
- ✅ "Board Game Night"
- ✅ "Soirée jeu conviviale"
- ✅ "Plateau du vendredi"
- ❌ "Réunion" (pas de mot-clé)
- ❌ "Cinema" (pas de mot-clé)

**Événements créés automatiquement** :
- 📅 Nom : "Soirée Plateaux - Vendredi DD mois AAAA"
- 🕖 Horaire : 20:30 - 00:30 (4 heures)
- 📍 Lieu : Configuré dans EVENT_LOCATION (événement externe)
- 📝 Description : Configurée dans EVENT_DESCRIPTION
- 🔒 Visibilité : Serveur uniquement

**Note** : Les événements créés automatiquement sont des événements individuels (non récurrents), permettant un meilleur suivi des inscriptions par soirée.

## 📝 Commandes disponibles

- `!create-plateau-post` : Crée ou met à jour le post pour le prochain vendredi
- `!process-next-month` : Traite les 4 prochains vendredis (création + mise à jour)
- `!plateau-next-month` : Alias pour !process-next-month
- `!process-friday YYYY-MM-DD` : **Nouveau** - Traite un vendredi spécifique (ex: `!process-friday 2025-12-26`)
- `!update-participants` : Force la mise à jour de la liste des inscriptions
- `!list-events` : Liste tous les événements Discord avec leurs IDs
- `!plateau-help` : Affiche l'aide des commandes
- `!test` : Teste la réception des messages

## 👥 Mise à Jour Automatique des Inscriptions

Le bot met à jour automatiquement la liste des personnes inscrites dans les posts de forum :
- ✅ **Vérification automatique** : Toutes les 15 minutes
- 👤 **Source** : Utilisateur·rice·s inscrit·e·s aux événements Discord
- 📊 **Affichage** : Nombre + noms des personnes (max 10 affichés)
- 🔄 **Temps réel** : Les posts se mettent à jour dès qu'une personne s'inscrit ou se désinscrit
- ♾️ **Écriture inclusive** : Le bot utilise des termes épicènes dans les logs (participant·e·s, inscrit·e·s)

**Exemple dans le post** :
```
👥 Inscriptions
12 personne(s) inscrite(s)
Alice, Bob, Charlie, David, Emma, Frank, Grace, Henry, Iris, Jack... et 2 autre(s)
```

**Dans les logs** :
```
🔍 Récupération des participant·e·s pour l'événement
👤 Participant·e trouvé·e sur l'événement principal: Alice
✅ Total: 12 personne·s inscrite·s (après déduplication)
```

## 🔧 Technologies utilisées

```mermaid
graph TB
    subgraph "🐍 Python Stack"
        PY[Python 3.11+]
        DPY[discord.py 2.3.2]
        DOTENV[python-dotenv]
        PYTZ[pytz]
        ASYNC[asyncio]
    end
    
    subgraph "🐳 Container"
        DOCKER[Docker]
        COMPOSE[Docker Compose]
        ALPINE[Python 3.11 Slim]
    end
    
    subgraph "☁️ Services"
        DISCORD[Discord API]
        GHCR[GitHub Container Registry]
        GA[GitHub Actions]
    end
    
    PY --> DPY
    PY --> DOTENV
    PY --> PYTZ
    PY --> ASYNC
    
    DOCKER --> ALPINE
    COMPOSE --> DOCKER
    ALPINE --> PY
    
    DPY <--> DISCORD
    GA --> GHCR
    GHCR --> DOCKER
    
    style PY fill:#1e5a8e,stroke:#1f6feb,stroke-width:2px,color:#fff
    style DPY fill:#161b22,stroke:#1f6feb,stroke-width:2px,color:#fff
    style DOTENV fill:#161b22,stroke:#1f6feb,stroke-width:2px,color:#fff
    style PYTZ fill:#161b22,stroke:#1f6feb,stroke-width:2px,color:#fff
    style ASYNC fill:#161b22,stroke:#1f6feb,stroke-width:2px,color:#fff
    style DOCKER fill:#0969da,stroke:#1f6feb,stroke-width:2px,color:#fff
    style COMPOSE fill:#161b22,stroke:#1f6feb,stroke-width:2px,color:#fff
    style ALPINE fill:#161b22,stroke:#1f6feb,stroke-width:2px,color:#fff
    style DISCORD fill:#404eed,stroke:#1f6feb,stroke-width:2px,color:#fff
    style GHCR fill:#1a7f37,stroke:#2ea043,stroke-width:2px,color:#fff
    style GA fill:#161b22,stroke:#1f6feb,stroke-width:2px,color:#fff
```

## 📦 Structure du projet

```
.
├── bot.py                      # Code principal du bot Python
├── requirements.txt            # Dépendances Python
├── Dockerfile.python           # Configuration Docker
├── docker-compose.python.yml   # Orchestration Docker
├── .env.example.python         # Exemple de configuration
└── README.python.md           # Cette documentation
```

## 🐳 Déploiement Docker

### Build local

```bash
docker build -f Dockerfile.python -t discord-plateau-bot-python .
```

### Lancer le conteneur

```bash
docker compose -f docker-compose.python.yml up -d
```

### Arrêter le bot

```bash
docker compose -f docker-compose.python.yml down
```

### Voir les logs

```bash
docker compose -f docker-compose.python.yml logs -f discord-bot-python
```

## 🔄 Planification automatique

Le bot crée automatiquement des posts tous les **samedis à 3h00** (fuseau horaire configurable).

Pour chaque vendredi, il :
1. Vérifie si un post existe déjà
2. Recherche l'événement Discord correspondant
3. Crée ou met à jour le post avec les informations actuelles

## 🆘 Dépannage

### Le bot ne répond pas aux commandes

- Vérifier que le bot a les permissions nécessaires
- Vérifier que l'intent `MESSAGE_CONTENT` est activé dans le Developer Portal
- Regarder les logs : `docker compose -f docker-compose.python.yml logs -f`

### Erreur de locale française

Le Dockerfile installe les locales françaises automatiquement. Si vous utilisez Python local :

```bash
# Sur Ubuntu/Debian
sudo apt-get install locales
sudo locale-gen fr_FR.UTF-8
```

### Problèmes de fuseau horaire

Vérifier la variable `TIMEZONE` dans `.env`. Liste des fuseaux : [pytz timezones](https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568)

## 📄 Licence

MIT

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## 🔐 Sécurité

- Ne jamais commiter le fichier `.env`
- Utiliser des secrets pour le déploiement en production
- Voir [SECURITY.md](SECURITY.md) pour plus de détails
