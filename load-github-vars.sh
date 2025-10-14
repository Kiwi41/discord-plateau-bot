#!/bin/bash

# Script pour utiliser les variables GitHub en local
# Compatible avec GitHub CLI (gh)

echo "🐙 Configuration depuis GitHub Secrets & Variables"
echo "=================================================="

# Vérifier si GitHub CLI est installé
if ! command -v gh &> /dev/null; then
    echo "⚠️  GitHub CLI (gh) non installé."
    echo "   Installation: https://cli.github.com/"
    echo "   Ou définissez les variables manuellement"
    echo
fi

# Vérifier l'authentification GitHub
if command -v gh &> /dev/null; then
    if ! gh auth status &>/dev/null; then
        echo "❌ Non authentifié avec GitHub"
        echo "   Exécutez: gh auth login"
        exit 1
    fi
fi

# Fonction pour récupérer une variable GitHub
get_github_variable() {
    local var_name=$1
    local var_type=${2:-"vars"}  # "vars" ou "secrets"
    
    # Méthode 1: Via GitHub CLI (si disponible et authentifié)
    if command -v gh &> /dev/null && gh auth status &>/dev/null; then
        local repo=$(gh repo view --json owner,name -q '.owner.login + "/" + .name' 2>/dev/null)
        if [ -n "$repo" ]; then
            if [ "$var_type" = "secrets" ]; then
                # Les secrets ne peuvent pas être lus via CLI pour des raisons de sécurité
                echo "⚠️  Secret $var_name ne peut pas être lu via CLI"
                return 1
            else
                local value=$(gh variable get $var_name 2>/dev/null || echo "")
                if [ -n "$value" ]; then
                    echo "$value"
                    return 0
                fi
            fi
        fi
    fi
    
    # Méthode 2: Depuis variables d'environnement locales (fallback)
    local env_value=$(eval echo \$$var_name)
    if [ -n "$env_value" ]; then
        echo "$env_value"
        return 0
    fi
    
    return 1
}

# Information sur les secrets
echo "🔐 Note: Les secrets GitHub ne peuvent pas être lus via API/CLI pour des raisons de sécurité"
echo "   Vous devez les définir manuellement en local :"
echo

# Charger les variables GitHub (publiques seulement)
echo "📥 Récupération des variables publiques depuis GitHub..."

# Variables Discord (publiques)
GUILD_ID=$(get_github_variable "GUILD_ID" "vars")
FORUM_CHANNEL_ID=$(get_github_variable "FORUM_CHANNEL_ID" "vars")
REGISTRATION_URL=$(get_github_variable "REGISTRATION_URL" "vars")
TIMEZONE=$(get_github_variable "TIMEZONE" "vars")

# Variables de déploiement (publiques)
DEPLOY_HOST=$(get_github_variable "DEPLOY_HOST" "vars")
DEPLOY_USER=$(get_github_variable "DEPLOY_USER" "vars")
SYNOLOGY_HOST=$(get_github_variable "SYNOLOGY_HOST" "vars")
SYNOLOGY_USER=$(get_github_variable "SYNOLOGY_USER" "vars")

echo "✅ Variables publiques récupérées:"
echo "   ✅ GUILD_ID: ${GUILD_ID:-'Non défini'}"
echo "   ✅ FORUM_CHANNEL_ID: ${FORUM_CHANNEL_ID:-'Non défini'}"
echo "   ✅ REGISTRATION_URL: ${REGISTRATION_URL:-'Non défini'}"
echo "   ✅ TIMEZONE: ${TIMEZONE:-'Non défini'}"

echo
echo "🔐 Variables secrètes à définir manuellement:"

# Vérifier les secrets depuis l'environnement
missing_secrets=()
[ -z "$DISCORD_TOKEN" ] && missing_secrets+=("DISCORD_TOKEN")

if [ ${#missing_secrets[@]} -gt 0 ]; then
    echo "   ❌ Manquants: ${missing_secrets[*]}"
    echo
    echo "💡 Pour définir les secrets localement :"
    echo "   export DISCORD_TOKEN=\"votre_token_discord\""
    echo "   export SSH_PRIVATE_KEY=\"\$(cat ~/.ssh/id_rsa)\""
    echo "   export SYNOLOGY_SSH_KEY=\"\$(cat ~/.ssh/synology_rsa)\""
    echo "   export DISCORD_WEBHOOK_URL=\"https://discord.com/api/webhooks/...\""
    echo
    echo "🔧 Puis relancez ce script:"
    echo "   ./load-github-vars.sh"
    exit 1
else
    echo "   ✅ DISCORD_TOKEN: $(echo $DISCORD_TOKEN | cut -c1-10)..."
fi

# Créer .env avec les variables GitHub
echo
echo "📝 Création du fichier .env..."
cat > .env << EOF
# Variables récupérées depuis GitHub Secrets & Variables
# Générées automatiquement le $(date)

DISCORD_TOKEN=${DISCORD_TOKEN}
GUILD_ID=${GUILD_ID}
FORUM_CHANNEL_ID=${FORUM_CHANNEL_ID}
REGISTRATION_URL=${REGISTRATION_URL:-https://votre-lien-inscription.com}
TIMEZONE=${TIMEZONE:-Europe/Paris}
EOF

# Exporter dans l'environnement actuel
export DISCORD_TOKEN="$DISCORD_TOKEN"
export GUILD_ID="$GUILD_ID"
export FORUM_CHANNEL_ID="$FORUM_CHANNEL_ID"
export REGISTRATION_URL="${REGISTRATION_URL:-https://votre-lien-inscription.com}"
export TIMEZONE="${TIMEZONE:-Europe/Paris}"

echo "✅ Variables GitHub configurées:"
echo "   ✅ DISCORD_TOKEN: $(echo $DISCORD_TOKEN | cut -c1-10)..."
echo "   ✅ GUILD_ID: $GUILD_ID"
echo "   ✅ FORUM_CHANNEL_ID: $FORUM_CHANNEL_ID"
echo "   ✅ REGISTRATION_URL: $REGISTRATION_URL"
echo "   ✅ TIMEZONE: $TIMEZONE"

echo
echo "🚀 Variables prêtes ! Commandes disponibles:"
echo "   docker compose up -d          # Démarrer le bot"
echo "   docker compose logs -f        # Voir les logs"
echo "   source $(basename $0)         # Charger dans shell actuel"

# Test optionnel de connectivité Discord
echo
echo "🧪 Test de connectivité Discord (optionnel):"
echo -n "   Tester la connexion ? (y/N): "
read -r test_connection

if [[ $test_connection =~ ^[Yy]$ ]]; then
    echo "   🔍 Test de l'image Docker..."
    if docker build -t discord-bot-test . >/dev/null 2>&1; then
        echo "   ✅ Build réussi"
        echo "   🔌 Test de connexion Discord..."
        timeout 30 docker run --rm --env-file .env discord-bot-test 2>&1 | head -10
        echo "   ✅ Test terminé"
    else
        echo "   ❌ Erreur lors du build"
    fi
fi

echo
echo "💡 Pour configurer GitHub Secrets & Variables:"
echo "   Repository → Settings → Secrets and variables → Actions"
echo "   Voir GITHUB_VARIABLES.md pour les détails"