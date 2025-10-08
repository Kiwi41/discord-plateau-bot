#!/bin/bash

echo "🔐 Configuration GitHub avec authentification directe"
echo
echo "Ton username GitHub : Kiwi41"
echo "Repository : discord-plateau-bot"
echo
echo "Pour créer un nouveau token avec les bonnes permissions :"
echo "1. Va sur : https://github.com/settings/tokens/new"
echo "2. Note/Description : 'Discord Bot Token'"
echo "3. Expiration : 90 days (ou plus)"
echo "4. Coches OBLIGATOIREMENT :"
echo "   ✅ repo (Full control of private repositories)"
echo "   ✅ workflow (Update GitHub Action workflows)"
echo "5. Clique sur 'Generate token'"
echo
echo -n "Colle ton nouveau token (ou confirme l'ancien) : "
read -s TOKEN
echo
echo

if [ -z "$TOKEN" ]; then
    echo "❌ Token vide !"
    exit 1
fi

echo "🔄 Test d'authentification..."

# Configuration Git globale temporaire
git config --global credential.helper store
git config --global user.name "Kiwi41"  
git config --global user.email "kevin.favry@gmail.com"

# Test d'authentification avec API GitHub
echo "🧪 Test API GitHub..."
RESPONSE=$(curl -s -H "Authorization: token $TOKEN" https://api.github.com/user)
USERNAME=$(echo $RESPONSE | grep -o '"login":"[^"]*' | cut -d'"' -f4)

if [ "$USERNAME" = "Kiwi41" ]; then
    echo "✅ Authentification API réussie pour $USERNAME"
else
    echo "❌ Problème d'authentification API"
    echo "Réponse : $RESPONSE"
    exit 1
fi

# Test d'accès au repository
echo "🧪 Test d'accès au repository..."
REPO_RESPONSE=$(curl -s -H "Authorization: token $TOKEN" https://api.github.com/repos/Kiwi41/discord-plateau-bot)
REPO_NAME=$(echo $REPO_RESPONSE | grep -o '"name":"[^"]*' | cut -d'"' -f4)

if [ "$REPO_NAME" = "discord-plateau-bot" ]; then
    echo "✅ Accès au repository confirmé"
else
    echo "❌ Problème d'accès au repository"
    echo "Réponse : $REPO_RESPONSE"
    exit 1
fi

echo
echo "🚀 Configuration Git pour push..."

# Supprime l'ancien remote et le reconfigure
git remote remove origin 2>/dev/null || true
git remote add origin https://$TOKEN@github.com/Kiwi41/discord-plateau-bot.git

echo "🚀 Push vers GitHub..."
git push -u origin main --force

if [ $? -eq 0 ]; then
    echo
    echo "🎉 SUCCÈS ! Code pushé vers GitHub !"
    echo "📖 Repository disponible sur : https://github.com/Kiwi41/discord-plateau-bot"
    echo
    echo "🧹 Nettoyage sécurisé..."
    # Reconfigure avec URL sans token pour la sécurité
    git remote remove origin
    git remote add origin https://github.com/Kiwi41/discord-plateau-bot.git
    git config --global --unset credential.helper 2>/dev/null || true
    echo "✅ Configuration nettoyée"
else
    echo "❌ Échec du push"
    git remote remove origin
    git remote add origin https://github.com/Kiwi41/discord-plateau-bot.git
fi