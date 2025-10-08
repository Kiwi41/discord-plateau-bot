#!/bin/bash

echo "🚀 Push final vers GitHub"
echo
echo -n "Ton token GitHub : "
read -s TOKEN
echo

if [ -z "$TOKEN" ]; then
    echo "❌ Token vide !"
    exit 1
fi

echo "🔗 Configuration du remote avec token..."
git remote add origin https://$TOKEN@github.com/Kiwi41/discord-plateau-bot.git

echo "🚀 Push vers GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo
    echo "🎉 SUCCÈS ! Code pushé vers GitHub !"
    echo "📖 Repository : https://github.com/Kiwi41/discord-plateau-bot"
    
    echo
    echo "🧹 Nettoyage sécurisé du token..."
    git remote remove origin
    git remote add origin https://github.com/Kiwi41/discord-plateau-bot.git
    echo "✅ Token supprimé de la configuration Git"
else
    echo "❌ Échec du push"
    git remote remove origin
    git remote add origin https://github.com/Kiwi41/discord-plateau-bot.git
fi