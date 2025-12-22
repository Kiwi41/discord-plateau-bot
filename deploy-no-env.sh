#!/bin/bash

# 🚀 Script de déploiement sans fichier .env
# Les secrets sont passés via variables d'environnement

echo "🔐 Configuration des variables d'environnement Discord Bot"
echo "========================================================="
echo ""

# Vérifier si les variables sont déjà définies
if [ -z "$DISCORD_TOKEN" ]; then
    echo "⚠️  Variables d'environnement non définies"
    echo ""
    echo "Définissez les variables avant de lancer ce script :"
    echo ""
    echo "export DISCORD_TOKEN='votre_token_bot'"
    echo "export GUILD_ID='votre_guild_id'"
    echo "export FORUM_CHANNEL_ID='votre_forum_channel_id'"
    echo "export REGISTRATION_URL='https://votre-lien-inscription.com'"
    echo "export EVENT_ID='votre_event_id_optionnel'"
    echo "export TIMEZONE='Europe/Paris'"
    echo ""
    echo "Puis relancez : ./deploy-no-env.sh"
    exit 1
fi

echo "✅ Variables d'environnement détectées"
echo "   Token: ${DISCORD_TOKEN:0:10}..."
echo "   Guild ID: $GUILD_ID"
echo "   Forum Channel ID: $FORUM_CHANNEL_ID"
echo "   Registration URL: $REGISTRATION_URL"
echo "   Timezone: ${TIMEZONE:-Europe/Paris}"
echo ""

# Lancer avec docker-compose
echo "🚀 Démarrage du bot avec docker-compose..."
docker compose -f docker-compose.system-env.yml pull
docker compose -f docker-compose.system-env.yml up -d

echo ""
echo "✅ Bot démarré !"
echo ""
echo "📋 Commandes utiles :"
echo "   Logs :      docker compose -f docker-compose.system-env.yml logs -f discord-bot"
echo "   Status :    docker compose -f docker-compose.system-env.yml ps"
echo "   Arrêter :   docker compose -f docker-compose.system-env.yml down"
