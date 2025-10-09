#!/bin/bash

echo "🚂 Migration vers Railway.app - Hébergement GRATUIT"
echo "=================================================="
echo

# Vérification des prérequis
if ! command -v npm &> /dev/null; then
    echo "❌ Node.js/npm requis. Installe d'abord Node.js"
    exit 1
fi

echo "📋 Étapes de migration :"
echo "1. Créer compte Railway"
echo "2. Connecter GitHub"  
echo "3. Déployer le projet"
echo "4. Configurer variables d'environnement"
echo "5. Arrêter Heroku"
echo

# Créer le fichier de configuration Railway
echo "⚙️ Création de railway.json..."
cat > railway.json << 'EOF'
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "node index.js",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
EOF

echo "✅ railway.json créé"

# Créer un fichier nixpacks.toml pour optimiser le build
echo "📦 Création de nixpacks.toml..."
cat > nixpacks.toml << 'EOF'
[phases.setup]
nixPkgs = ["nodejs_18", "npm"]

[phases.install]
cmds = ["npm ci"]

[phases.build]
cmds = ["echo 'No build step needed'"]

[start]
cmd = "node index.js"
EOF

echo "✅ nixpacks.toml créé"

# Instructions détaillées
echo "📖 INSTRUCTIONS DÉTAILLÉES :"
echo
echo "🌐 1. Va sur https://railway.app et crée un compte"
echo "   • Utilise ton compte GitHub pour te connecter"
echo
echo "📁 2. Crée un nouveau projet :"
echo "   • Clique 'New Project'"
echo "   • Sélectionne 'Deploy from GitHub repo'"  
echo "   • Choisis 'Kiwi41/discord-plateau-bot'"
echo
echo "⚙️ 3. Configure les variables d'environnement :"
echo "   • Va dans Settings > Variables"
echo "   • Ajoute TOUTES les variables de .env :"

# Lire les variables du fichier .env et les afficher (sans valeurs sensibles)
if [ -f ".env" ]; then
    echo
    echo "📋 Variables à configurer :"
    while IFS= read -r line; do
        if [[ $line == *"="* ]] && [[ $line != "#"* ]]; then
            var_name=$(echo "$line" | cut -d'=' -f1)
            echo "   • $var_name"
        fi
    done < .env
fi

echo
echo "🚀 4. Déploiement automatique :"
echo "   • Railway détecte package.json"
echo "   • Build automatique avec 'npm install'"
echo "   • Start avec 'node index.js'"
echo "   • Le bot démarre en ~30 secondes"
echo
echo "✋ 5. Arrêter Heroku (après vérification) :"
echo "   • heroku ps:scale worker=0 -a discord-plateau-bot"
echo "   • Ou supprimer l'app : heroku apps:destroy discord-plateau-bot"
echo

# Créer un script de vérification
echo "🔍 Script de vérification Railway..."
cat > scripts/deployment/check-railway.sh << 'EOF'
#!/bin/bash

echo "🔍 Vérification du déploiement Railway"
echo "====================================="

echo "📋 Checklist post-déploiement :"
echo "□ Bot connecté sur Discord ?"
echo "□ Logs Railway sans erreurs ?"
echo "□ Variables d'environnement configurées ?"
echo "□ Commandes slash fonctionnelles ?"
echo "□ Cron job samedi 3h programmé ?"
echo

echo "🔗 Liens utiles :"
echo "• Dashboard Railway : https://railway.app/dashboard"
echo "• Logs en direct : https://railway.app/project/[ton-projet]/service/[ton-service]"
echo "• Variables : https://railway.app/project/[ton-projet]/service/[ton-service]/variables"

echo
echo "⚠️ Si tout fonctionne, tu peux arrêter Heroku :"
echo "heroku ps:scale worker=0 -a discord-plateau-bot"
EOF

chmod +x scripts/deployment/check-railway.sh

echo "✅ Scripts créés dans scripts/deployment/"
echo
echo "💰 ÉCONOMIES :"
echo "• Heroku : $7/mois = $84/an"
echo "• Railway : $0/mois = $0/an" 
echo "• 💸 ÉCONOMIE : $84/an !"
echo
echo "🎯 NEXT STEPS :"
echo "1. 🌐 Crée ton compte sur https://railway.app"
echo "2. 📂 Connecte ce repo GitHub"
echo "3. ⚙️ Configure les variables d'env"
echo "4. 🚀 Deploy !"
echo "5. ✅ Vérifie avec ./scripts/deployment/check-railway.sh"
echo
echo "⏱️ Temps estimé : 10-15 minutes"