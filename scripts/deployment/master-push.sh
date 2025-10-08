#!/bin/bash

echo "🚀 Push final vers GitHub (branche master)"
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

echo "🚀 Push vers GitHub (master)..."
git push -u origin master

if [ $? -eq 0 ]; then
    echo
    echo "🎉 SUCCÈS ! Code pushé vers GitHub !"
    echo "📖 Repository : https://github.com/Kiwi41/discord-plateau-bot"
    echo "📚 Documentation : https://github.com/Kiwi41/discord-plateau-bot/blob/master/README.md"
    
    echo
    echo "🧹 Nettoyage sécurisé du token..."
    git remote remove origin
    git remote add origin https://github.com/Kiwi41/discord-plateau-bot.git
    echo "✅ Token supprimé de la configuration Git"
else
    echo "❌ Échec du push - erreur détaillée :"
    git push -u origin master 2>&1
    git remote remove origin
    git remote add origin https://github.com/Kiwi41/discord-plateau-bot.git
fi