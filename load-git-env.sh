#!/bin/bash

# Script pour charger les variables depuis Git config
echo "📦 Chargement des variables depuis Git config"
echo "============================================="

# Fonction pour récupérer et exporter les variables Git
load_from_git_config() {
    local discord_token=$(git config discord.token 2>/dev/null)
    local guild_id=$(git config discord.guild-id 2>/dev/null)
    local forum_channel_id=$(git config discord.forum-channel-id 2>/dev/null)
    local registration_url=$(git config discord.registration-url 2>/dev/null)
    local timezone=$(git config discord.timezone 2>/dev/null)
    
    # Vérifier si les variables sont configurées
    if [ -z "$discord_token" ] || [ -z "$guild_id" ] || [ -z "$forum_channel_id" ]; then
        echo "❌ Variables Git non configurées !"
        echo "   Exécutez d'abord: ./setup-git-config.sh"
        return 1
    fi
    
    # Exporter les variables
    export DISCORD_TOKEN="$discord_token"
    export GUILD_ID="$guild_id"
    export FORUM_CHANNEL_ID="$forum_channel_id"
    export REGISTRATION_URL="${registration_url:-https://votre-lien-inscription.com}"
    export TIMEZONE="${timezone:-Europe/Paris}"
    
    echo "✅ Variables chargées depuis Git config:"
    echo "   ✅ DISCORD_TOKEN: $(echo $DISCORD_TOKEN | cut -c1-10)..."
    echo "   ✅ GUILD_ID: $GUILD_ID"
    echo "   ✅ FORUM_CHANNEL_ID: $FORUM_CHANNEL_ID"
    echo "   ✅ REGISTRATION_URL: $REGISTRATION_URL"
    echo "   ✅ TIMEZONE: $TIMEZONE"
    
    return 0
}

# Charger les variables
if load_from_git_config; then
    echo
    echo "🚀 Variables prêtes ! Vous pouvez maintenant lancer:"
    echo "   docker compose up -d"
    echo
    echo "💡 Pour rendre permanent, ajoutez à votre ~/.zshrc:"
    echo "   source $(pwd)/load-git-env.sh"
else
    exit 1
fi