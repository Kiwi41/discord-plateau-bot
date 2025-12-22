# 🎲 Discord Bot pour Soirées Plateaux - Version Python

Bot Discord automatisé qui crée des posts hebdomadaires dans un forum pour planifier les soirées jeux de plateau du vendredi soir.

## ✨ Fonctionnalités

- **📅 Création automatique** : Posts hebdomadaires chaque samedi à 3h00
- **🎯 Intégration forum** : Utilise les forums Discord natifs
- **🔗 Liens automatiques** : Vers les événements Discord et inscription
- **⚡ Commandes manuelles** : Création manuelle et gestion avancée
- **🐳 Docker** : Déploiement conteneurisé sur NAS, cloud ou local
- **🐍 Python 3.11+** : Code moderne et maintenable

## 🚀 Installation Rapide

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
EVENT_ID=votre_event_id_optionnel
TIMEZONE=Europe/Paris
```

### 🔑 Obtenir les tokens Discord

1. **Token Bot** : [Discord Developer Portal](https://discord.com/developers/applications)
   - Créer une application → Bot → Copy Token
   
2. **Guild ID** : Clic droit sur votre serveur → "Copier l'identifiant"

3. **Forum Channel ID** : Clic droit sur votre canal forum → "Copier l'identifiant"

4. **Event ID** (optionnel) : ID de l'événement récurrent Discord

## 📝 Commandes disponibles

- `!create-plateau-post` : Crée ou met à jour le post pour le prochain vendredi
- `!process-next-month` : Traite les 4 prochains vendredis (création + mise à jour)
- `!plateau-next-month` : Alias pour !process-next-month
- `!plateau-help` : Affiche l'aide des commandes
- `!test` : Teste la réception des messages

## 🔧 Technologies utilisées

- **discord.py 2.3.2** : Bibliothèque Discord pour Python
- **python-dotenv** : Gestion des variables d'environnement
- **pytz** : Support des fuseaux horaires
- **asyncio** : Programmation asynchrone native Python

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
