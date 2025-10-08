#!/bin/bash

TOKEN_FILE="$HOME/.github-token-discord-bot"

echo "🚀 Push automatique vers GitHub avec token stocké"
echo

# Vérification du token stocké
if [ ! -f "$TOKEN_FILE" ]; then
    echo "❌ Aucun token stocké trouvé !"
    echo "📋 Lance d'abord : ./store-token.sh"
    exit 1
fi

# Vérification des permissions du fichier token
TOKEN_PERMS=$(stat -c "%a" "$TOKEN_FILE" 2>/dev/null)
if [ "$TOKEN_PERMS" != "600" ]; then
    echo "🔒 Correction des permissions du token..."
    chmod 600 "$TOKEN_FILE"
fi

# Chargement du token
TOKEN=$(cat "$TOKEN_FILE")

if [ -z "$TOKEN" ]; then
    echo "❌ Token vide dans le fichier !"
    exit 1
fi

echo "✅ Token chargé depuis $TOKEN_FILE"
echo

# Ajout des fichiers non trackés si il y en a
if [ -n "$(git status --porcelain)" ]; then
    echo "📁 Ajout des nouveaux fichiers..."
    git add .
    
    if [ -n "$(git status --porcelain --cached)" ]; then
        echo "💾 Création d'un commit..."
        git commit -m "feat: update project files - $(date '+%Y-%m-%d %H:%M')"
    fi
fi

echo "🔗 Configuration du remote avec token..."
git remote remove origin 2>/dev/null || true
git remote add origin https://$TOKEN@github.com/Kiwi41/discord-plateau-bot.git

echo "🚀 Push vers GitHub (master)..."
git push -u origin master

if [ $? -eq 0 ]; then
    echo
    echo "🎉 SUCCÈS ! Code pushé vers GitHub !"
    echo "📖 Repository : https://github.com/Kiwi41/discord-plateau-bot"
    echo "📚 Documentation : https://github.com/Kiwi41/discord-plateau-bot/blob/master/docs/README.md"
    echo
    echo "📋 Contenu pushé :"
    echo "   ✅ Bot Discord (index.js)"
    echo "   ✅ Documentation complète (/docs/)"
    echo "   ✅ 6 diagrammes Graphviz"
    echo "   ✅ Configuration Heroku"
    echo "   ✅ Scripts d'automatisation"
else
    echo "❌ Échec du push"
    echo "🔍 Détails de l'erreur :"
    git push -u origin master 2>&1 | head -10
fi

echo
echo "🧹 Nettoyage sécurisé..."
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/Kiwi41/discord-plateau-bot.git
echo "✅ Token supprimé de la configuration Git"