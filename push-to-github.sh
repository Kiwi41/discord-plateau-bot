#!/bin/bash

echo "🚀 Push vers GitHub - discord-plateau-bot"
echo "================================================"
echo
echo "📋 Configuration actuelle :"
echo "   Repository : https://github.com/Kiwi41/discord-plateau-bot"
echo "   Utilisateur: $(git config user.name) <$(git config user.email)>"
echo "   Credential : $(git config credential.username)"
echo
echo "🔑 Authentification requise :"
echo "   Username: Kiwi41 (ou kiwi)"
echo "   Password: [Personal Access Token GitHub]"
echo
echo "💡 Si tu n'as pas encore de token :"
echo "   1. Va sur https://github.com/settings/tokens"
echo "   2. 'Generate new token (classic)'"
echo "   3. Sélectionne 'repo' comme permission"
echo "   4. Copie le token généré"
echo
echo "⏳ Démarrage du push..."
echo

# Tentative de push
git push -u origin master

exit_code=$?

echo
if [ $exit_code -eq 0 ]; then
    echo "✅ Push réussi !"
    echo "🌐 Ton repository est maintenant disponible :"
    echo "   https://github.com/Kiwi41/discord-plateau-bot"
else
    echo "❌ Push échoué (code: $exit_code)"
    echo
    echo "🔧 Solutions possibles :"
    echo "1. Vérifier que le token GitHub est valide"
    echo "2. S'assurer que les permissions 'repo' sont activées"
    echo "3. Essayer de vider le cache : git credential-cache exit"
    echo "4. Réessayer le push"
fi

echo
echo "📊 Statut du repository :"
git status --porcelain
echo
echo "📋 Derniers commits :"
git log --oneline -3