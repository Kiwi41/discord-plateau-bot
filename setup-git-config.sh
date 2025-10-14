#!/bin/bash

# Configuration Git pour les variables Discord
echo "🔧 Configuration des variables Git locales"
echo "=========================================="

# Configurer les variables dans Git (local au repo)
git config discord.token "${DISCORD_TOKEN:-}"
git config discord.guild-id "${GUILD_ID:-}"
git config discord.forum-channel-id "${FORUM_CHANNEL_ID:-}"
git config discord.registration-url "${REGISTRATION_URL:-https://votre-lien-inscription.com}"
git config discord.timezone "${TIMEZONE:-Europe/Paris}"

echo "✅ Variables Git configurées localement"
echo
echo "🔍 Vérification:"
echo "   Token: $(git config discord.token | cut -c1-10)..."
echo "   Guild ID: $(git config discord.guild-id)"
echo "   Forum Channel ID: $(git config discord.forum-channel-id)"
echo "   Registration URL: $(git config discord.registration-url)"
echo "   Timezone: $(git config discord.timezone)"

echo
echo "💡 Pour utiliser ces variables:"
echo "   export DISCORD_TOKEN=\$(git config discord.token)"
echo "   export GUILD_ID=\$(git config discord.guild-id)"
echo "   export FORUM_CHANNEL_ID=\$(git config discord.forum-channel-id)"