#!/bin/bash

# Script de configuration sécurisé pour le bot Discord
# Ce script configure les variables d'environnement de façon sécurisée

echo "🔐 Configuration sécurisée du Bot Discord Soirées Plateaux"
echo "=========================================================="
echo

# Vérifier que .env n'est pas commité
if git ls-files --error-unmatch .env >/dev/null 2>&1; then
    echo "⚠️  ATTENTION: .env est tracké par Git !"
    echo "   Exécutez: git rm --cached .env"
    echo "   Puis: git commit -m 'Remove .env from tracking'"
    exit 1
fi

# Créer .env à partir du template si nécessaire
if [ ! -f .env ]; then
    echo "📄 Création du fichier .env à partir du template..."
    cp .env.template .env
    echo "✅ Fichier .env créé"
else
    echo "📄 Fichier .env existant détecté"
fi

echo
echo "🔑 Configuration des variables Discord:"
echo "======================================"

# Fonction pour demander une variable de façon sécurisée
ask_variable() {
    local var_name=$1
    local description=$2
    local current_value
    
    current_value=$(grep "^$var_name=" .env 2>/dev/null | cut -d'=' -f2)
    
    if [ -n "$current_value" ] && [ "$current_value" != "your_${var_name,,}_here" ]; then
        echo "✅ $var_name déjà configuré"
    else
        echo
        echo "📝 $description"
        echo -n "   Entrez $var_name: "
        
        if [[ "$var_name" == "DISCORD_TOKEN" ]]; then
            # Masquer l'entrée pour le token
            read -s new_value
            echo
        else
            read new_value
        fi
        
        # Mettre à jour .env
        if grep -q "^$var_name=" .env; then
            # Utiliser un délimiteur différent pour éviter les conflits avec /
            sed -i "s|^$var_name=.*|$var_name=$new_value|" .env
        else
            echo "$var_name=$new_value" >> .env
        fi
        echo "✅ $var_name configuré"
    fi
}

# Configurer chaque variable
ask_variable "DISCORD_TOKEN" "Token de votre bot Discord (depuis https://discord.com/developers/applications)"
ask_variable "GUILD_ID" "ID de votre serveur Discord (clic droit > Copier l'identifiant)"
ask_variable "FORUM_CHANNEL_ID" "ID du canal forum planning-plateau"

# Variables optionnelles
echo
echo "⚙️ Configuration optionnelle:"
echo "============================"

current_url=$(grep "^REGISTRATION_URL=" .env 2>/dev/null | cut -d'=' -f2-)
if [ -z "$current_url" ] || [ "$current_url" = "https://votre-lien-inscription.com" ]; then
    echo -n "📝 URL d'inscription (optionnel): "
    read registration_url
    if [ -n "$registration_url" ]; then
        if grep -q "^REGISTRATION_URL=" .env; then
            sed -i "s|^REGISTRATION_URL=.*|REGISTRATION_URL=$registration_url|" .env
        else
            echo "REGISTRATION_URL=$registration_url" >> .env
        fi
    fi
fi

# Timezone
current_tz=$(grep "^TIMEZONE=" .env 2>/dev/null | cut -d'=' -f2)
if [ -z "$current_tz" ]; then
    echo "TIMEZONE=Europe/Paris" >> .env
    echo "✅ Timezone définie sur Europe/Paris"
fi

echo
echo "🎉 Configuration terminée !"
echo "========================="
echo
echo "🔍 Vérification de la configuration:"
echo "   ✅ DISCORD_TOKEN: $(grep -q '^DISCORD_TOKEN=.*[^_here]$' .env && echo 'Configuré' || echo 'Manquant')"
echo "   ✅ GUILD_ID: $(grep -q '^GUILD_ID=.*[^_here]$' .env && echo 'Configuré' || echo 'Manquant')"
echo "   ✅ FORUM_CHANNEL_ID: $(grep -q '^FORUM_CHANNEL_ID=.*[^_here]$' .env && echo 'Configuré' || echo 'Manquant')"
echo
echo "🚀 Vous pouvez maintenant lancer le bot:"
echo "   docker compose up -d"
echo
echo "🔐 Sécurité:"
echo "   • .env est dans .gitignore (ne sera pas commité)"
echo "   • Ne partagez jamais votre fichier .env"
echo "   • Régénérez votre token Discord si compromis"