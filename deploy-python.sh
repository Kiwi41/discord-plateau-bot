#!/bin/bash

# Script de déploiement du bot Discord Python avec Docker

set -e

echo "🐳 Déploiement du Bot Discord Python"
echo "===================================="

# Vérifier si Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé"
    echo "   Installation: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé"
    echo "   Installation: https://docs.docker.com/compose/install/"
    exit 1
fi

# Vérifier si le fichier .env existe
if [ ! -f .env ]; then
    echo "⚠️  Fichier .env introuvable"
    
    if [ -f .env.example.python ]; then
        echo "📝 Copie de .env.example.python vers .env..."
        cp .env.example.python .env
        echo "✅ Fichier .env créé"
        echo ""
        echo "⚠️  IMPORTANT: Éditez le fichier .env avec vos vraies valeurs:"
        echo "   - DISCORD_TOKEN"
        echo "   - GUILD_ID"
        echo "   - FORUM_CHANNEL_ID"
        echo ""
        read -p "Appuyez sur Entrée après avoir configuré .env..."
    else
        echo "❌ .env.example.python introuvable"
        exit 1
    fi
fi

# Demander le mode de déploiement
echo ""
echo "Mode de déploiement:"
echo "  1) Build local (docker-compose.python.yml)"
echo "  2) Image pré-construite (docker-compose.prod.python.yml)"
echo ""
read -p "Choisissez (1 ou 2): " mode

case $mode in
    1)
        COMPOSE_FILE="docker-compose.python.yml"
        echo "📦 Build de l'image Docker..."
        docker compose -f $COMPOSE_FILE build
        ;;
    2)
        COMPOSE_FILE="docker-compose.prod.python.yml"
        echo "📥 Pull de l'image depuis le registre..."
        docker compose -f $COMPOSE_FILE pull || {
            echo "⚠️  Impossible de pull l'image, utilisation du build local..."
            COMPOSE_FILE="docker-compose.python.yml"
            docker compose -f $COMPOSE_FILE build
        }
        ;;
    *)
        echo "❌ Choix invalide"
        exit 1
        ;;
esac

# Arrêter le conteneur existant s'il existe
echo ""
echo "🔄 Arrêt du conteneur existant..."
docker compose -f $COMPOSE_FILE down 2>/dev/null || true

# Démarrer le bot
echo ""
echo "🚀 Démarrage du bot Discord Python..."
docker compose -f $COMPOSE_FILE up -d

# Attendre un peu que le bot démarre
sleep 3

# Afficher les logs
echo ""
echo "📋 Logs du bot:"
echo "=============="
docker compose -f $COMPOSE_FILE logs --tail=20

echo ""
echo "✅ Bot déployé avec succès!"
echo ""
echo "📝 Commandes utiles:"
echo "   - Voir les logs:        docker compose -f $COMPOSE_FILE logs -f"
echo "   - Arrêter le bot:       docker compose -f $COMPOSE_FILE down"
echo "   - Redémarrer le bot:    docker compose -f $COMPOSE_FILE restart"
echo "   - Status du bot:        docker compose -f $COMPOSE_FILE ps"
