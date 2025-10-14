# 🐙 Configuration GitHub Secrets & Variables

Ce guide explique comment configurer les variables d'environnement Discord dans GitHub pour un déploiement sécurisé.

## 🔐 Variables GitHub Required

Dans **Settings > Secrets and variables > Actions**, configurer :

### 🔒 Repository Secrets (Optionnelles)

| Secret | Valeur | Description |
|--------|--------|-------------|
| `DISCORD_WEBHOOK_URL` | `https://discord.com/api/webhooks/...` | Webhook notifications (optionnel) |

### 📋 Repository Variables (Non nécessaires pour CI/CD)

Les variables suivantes ne sont nécessaires que pour le déploiement local :

| Variable | Valeur | Description |
|----------|--------|-------------|
| `GUILD_ID` | `689502139621703691` | ID du serveur Discord |
| `FORUM_CHANNEL_ID` | `1424088409772789941` | ID du canal forum |
| `REGISTRATION_URL` | `https://votre-lien.com` | URL d'inscription |
| `TIMEZONE` | `Europe/Paris` | Fuseau horaire |

**Note**: Ces variables ne sont pas utilisées dans le pipeline CI/CD, seulement pour le déploiement manuel local.

## 📝 Configuration Étape par Étape

### 1. Accéder aux Secrets GitHub

```
Votre Repo → Settings → Secrets and variables → Actions
```

### 2. Configuration Minimale (Optionnelle)

La CI/CD ne nécessite aucune variable obligatoire ! Elle build et push l'image automatiquement.

#### DISCORD_WEBHOOK_URL (Optionnel)
- **Name** : `DISCORD_WEBHOOK_URL`  
- **Secret** : `https://discord.com/api/webhooks/your_webhook_id/your_webhook_token`
- **Description** : Notifications Discord des builds
- Cliquer **"Add secret"**

**C'est tout !** 🎉 La CI/CD fonctionne sans autres variables.

## 🚀 Workflow GitHub Actions

### 🏗️ Pipeline Automatique

À chaque push sur `main`, GitHub Actions :

1. **🧪 Test** : Build de l'image Docker
2. **🏗️ Build** : Construction et push vers `ghcr.io/kiwi41/discord-plateau-bot:latest`
3. **📢 Notify** : Notification Discord (si webhook configuré)

**Aucune variable requise !** Le pipeline fonctionne out-of-the-box.

### 📦 Déploiement Manuel sur NAS

Une fois l'image buildée, déployez manuellement :

```bash
# Sur votre NAS Synology
cd /volume1/docker/discord-plateau-bot

# Configurer les variables locales
cat > .env << EOF
DISCORD_TOKEN=votre_token
GUILD_ID=689502139621703691
FORUM_CHANNEL_ID=1424088409772789941
REGISTRATION_URL=https://votre-lien.com
TIMEZONE=Europe/Paris
EOF

# Utiliser l'image GitHub
docker pull ghcr.io/kiwi41/discord-plateau-bot:latest
docker compose up -d
```

## 🔍 Test des Variables

### Vérification Locale

```bash
# Test si les variables sont définies
echo "Discord Token: ${DISCORD_TOKEN:0:10}..."
echo "Guild ID: $GUILD_ID"
echo "Forum Channel: $FORUM_CHANNEL_ID"
```

### Debug Pipeline GitLab

```yaml
debug:variables:
  stage: test
  script:
    - echo "🔍 Variables disponibles:"
    - echo "Token présent: $([ -n "$DISCORD_TOKEN" ] && echo 'OUI' || echo 'NON')"
    - echo "Guild ID: $GUILD_ID" 
    - echo "Forum Channel: $FORUM_CHANNEL_ID"
    - echo "Registration URL: $REGISTRATION_URL"
    - echo "Timezone: $TIMEZONE"
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: manual
```

## 🛡️ Sécurité GitLab

### Variables Masked
- ✅ **DISCORD_TOKEN** : Masqué dans les logs
- ✅ **SSH_PRIVATE_KEY** : Masqué dans les logs  
- ✅ **DEPLOY_HOST** : Masqué si contient IP privée

### Variables Protected
- ✅ Disponibles seulement sur branches protégées (main/master)
- ✅ Disponibles seulement pour les tags
- ✅ Pas d'accès depuis les forks

### Bonnes Pratiques
- 🔐 Toujours masquer les tokens/clés
- 🛡️ Protéger les variables sensibles
- 📋 Documenter les variables requises
- 🔄 Rotation régulière des tokens

## 📞 Support

### Erreurs Communes

**Variables non trouvées**
```bash
# Vérifier la configuration GitLab
Project → Settings → CI/CD → Variables
```

**Token masqué incorrectement**
```bash
# Le token ne doit pas contenir d'espaces
# Longueur attendue: 70+ caractères
```

**Variables non disponibles**
```bash
# Vérifier les règles (rules) du job
# Variables protégées = branches protégées seulement
```

### Debug
```bash
# Dans un job GitLab CI
- env | grep DISCORD
- echo "CI Branch: $CI_COMMIT_BRANCH" 
- echo "Protected: $CI_COMMIT_REF_PROTECTED"
```

---

**🦊 GitLab CI/CD permet une gestion centralisée et sécurisée des variables sensibles !**