#!/bin/bash

TOKEN_FILE="$HOME/.github-token-discord-bot"

echo "🔐 Stockage sécurisé du token GitHub"
echo
echo "Ce script va stocker ton token dans : $TOKEN_FILE"
echo "Le fichier sera protégé (chmod 600 - lecture seule par toi)"
echo

if [ -f "$TOKEN_FILE" ]; then
    echo "⚠️  Un token existe déjà."
    echo -n "Veux-tu le remplacer ? (y/N) : "
    read -r REPLACE
    if [[ ! "$REPLACE" =~ ^[Yy]$ ]]; then
        echo "❌ Annulé"
        exit 0
    fi
fi

echo
echo -n "Colle ton token GitHub : "
read -s TOKEN
echo

if [ -z "$TOKEN" ]; then
    echo "❌ Token vide !"
    exit 1
fi

# Stockage sécurisé
echo "$TOKEN" > "$TOKEN_FILE"
chmod 600 "$TOKEN_FILE"

echo "✅ Token stocké de manière sécurisée dans $TOKEN_FILE"
echo "🔒 Permissions réglées sur 600 (lecture seule par toi)"
echo
echo "💡 Tu peux maintenant utiliser auto-push.sh qui chargera automatiquement le token"