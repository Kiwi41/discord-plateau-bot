#!/bin/bash

echo "🔐 Configuration sécurisée du token GitHub"
echo "=========================================="
echo
echo "⚠️  IMPORTANT : Ton token ne sera pas affiché ni stocké de façon permanente"
echo

# Demander le token de façon sécurisée (sans l'afficher)
read -s -p "🔑 Entre ton Personal Access Token GitHub : " GITHUB_TOKEN
echo
echo

if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ Aucun token fourni. Annulation."
    exit 1
fi

echo "✅ Token reçu (longueur: ${#GITHUB_TOKEN} caractères)"
echo

# Configuration de l'URL avec le token
echo "🔧 Configuration de l'URL GitHub avec le token..."
git remote set-url origin "https://kiwi:${GITHUB_TOKEN}@github.com/Kiwi41/discord-plateau-bot.git"

if [ $? -eq 0 ]; then
    echo "✅ URL configurée avec succès"
else
    echo "❌ Erreur lors de la configuration de l'URL"
    exit 1
fi

echo
echo "🚀 Tentative de push vers GitHub..."
echo

# Push vers GitHub
git push -u origin master

exit_code=$?

echo
if [ $exit_code -eq 0 ]; then
    echo "🎉 SUCCESS ! Push réussi !"
    echo
    echo "🌐 Ton repository est maintenant disponible sur :"
    echo "   https://github.com/Kiwi41/discord-plateau-bot"
    echo
    echo "📊 Contenu pushé :"
    echo "   • Code du bot Discord (index.js, config.js, etc.)"
    echo "   • Documentation complète (docs/ avec 21 fichiers)"
    echo "   • Diagrammes SVG (6 diagrammes Graphviz)"
    echo "   • Configuration Heroku (Procfile, package.json)"
    echo "   • Total : $(git ls-files | wc -l) fichiers"
else
    echo "❌ Push échoué (code: $exit_code)"
    echo
    echo "🔧 Vérifications possibles :"
    echo "1. Token valide avec permission 'repo'"
    echo "2. Repository existe sur GitHub"
    echo "3. Connexion internet stable"
fi

echo
echo "🧹 Nettoyage sécurisé..."
# Retirer le token de l'URL pour la sécurité
git remote set-url origin "https://github.com/Kiwi41/discord-plateau-bot.git"
echo "✅ Token supprimé de la configuration Git locale"

echo
echo "📋 Statut final :"
git status --short

# Effacer la variable
unset GITHUB_TOKEN