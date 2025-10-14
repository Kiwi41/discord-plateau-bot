# 🔐 Guide de Sécurité - Configuration des Variables

## ⚠️ Actions Urgentes

**IMPORTANT** : Si vous voyez des vraies valeurs dans `.env`, suivez ces étapes immédiatement :

1. **Régénérer le token Discord** :
   - Allez sur [Discord Developer Portal](https://discord.com/developers/applications)
   - Sélectionnez votre application → Bot → Reset Token
   - ⚠️ L'ancien token sera immédiatement invalide

2. **Configurer les variables système** :
   ```bash
   # Exporter les variables dans votre shell
   export DISCORD_TOKEN="votre_nouveau_token"
   export GUILD_ID="votre_guild_id"
   export FORUM_CHANNEL_ID="votre_forum_channel_id"
   export REGISTRATION_URL="votre_lien_inscription"
   export TIMEZONE="Europe/Paris"
   ```

3. **Rendre permanent** (ajoutez à `~/.bashrc` ou `~/.zshrc`) :
   ```bash
   # Variables Discord Bot
   export DISCORD_TOKEN="votre_nouveau_token"
   export GUILD_ID="votre_guild_id"
   export FORUM_CHANNEL_ID="votre_forum_channel_id"
   export REGISTRATION_URL="votre_lien_inscription"
   export TIMEZONE="Europe/Paris"
   ```

## 🚀 Méthodes de Configuration

### Méthode 1: Script Automatisé (Recommandé)

```bash
# Utiliser le script de configuration sécurisé
./setup-config.sh
```

Ce script :
- ✅ Vérifie que .env n'est pas tracké par Git
- ✅ Demande les tokens de façon sécurisée (masqué pour DISCORD_TOKEN)
- ✅ Crée un .env local non-commité
- ✅ Valide la configuration

### Méthode 2: Variables d'Environnement Système

```bash
# Dans votre ~/.zshrc ou ~/.bashrc
export DISCORD_TOKEN="votre_token"
export GUILD_ID="votre_guild_id"
export FORUM_CHANNEL_ID="votre_forum_channel_id"

# Recharger le shell
source ~/.zshrc
```

### Méthode 3: Docker Secrets (Production)

```yaml
# docker-compose.override.yml (local, non-commité)
services:
  plateau-bot:
    environment:
      - DISCORD_TOKEN=votre_token
      - GUILD_ID=votre_guild_id
      - FORUM_CHANNEL_ID=votre_forum_channel_id
```

### Méthode 4: NAS Synology

Dans Container Manager :
1. **Variables** → Add
2. **Name** : `DISCORD_TOKEN`
3. **Value** : `votre_token`
4. Répéter pour chaque variable

### Méthode 5: Heroku

```bash
# Via CLI
heroku config:set DISCORD_TOKEN=votre_token
heroku config:set GUILD_ID=votre_guild_id
heroku config:set FORUM_CHANNEL_ID=votre_forum_channel_id

# Ou via Dashboard web → Settings → Config Vars
```

## 🛡️ Bonnes Pratiques de Sécurité

### ✅ À Faire
- **Utilisez des variables d'environnement** système
- **Régénérez les tokens** si compromis
- **Limitez les permissions** du bot Discord
- **Sauvegardez les tokens** dans un gestionnaire de mots de passe
- **Vérifiez .gitignore** contient `.env`

### ❌ À Éviter
- **Jamais de tokens** dans le code source
- **Jamais commiter** `.env` avec vraies valeurs
- **Jamais partager** les tokens en clair
- **Jamais logs** contenant des tokens
- **Jamais screenshots** avec des tokens visibles

## 🔍 Vérification de Sécurité

```bash
# Vérifier que .env n'est pas tracké
git status --ignored

# Vérifier les variables d'environnement
echo $DISCORD_TOKEN | wc -c  # Doit retourner > 50

# Test du bot
docker compose up --abort-on-container-exit
```

## 🆘 En Cas de Compromission

1. **Immédiat** : Reset token Discord
2. **Vérifier** : Activité suspecte sur le serveur
3. **Analyser** : Logs Discord et serveur
4. **Informer** : Admin serveur si nécessaire
5. **Documenter** : Incident pour éviter répétition

## 📞 Support

- **Discord Developer** : [Support Portal](https://support.discord.com/hc/en-us/requests/new)
- **Bot Issues** : [GitHub Issues](https://github.com/Kiwi41/discord-plateau-bot/issues)
- **Sécurité** : Email privé aux mainteneurs

---

**🔐 La sécurité n'est pas optionnelle - protégez vos tokens comme vos mots de passe !**