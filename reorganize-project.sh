#!/bin/bash

echo "🧹 Nettoyage et réorganisation du projet Discord Bot"
echo "=================================================="
echo

# Créer la nouvelle structure
echo "📂 Création de la nouvelle arborescence..."

# Scripts utilitaires
mkdir -p "scripts/deployment"
mkdir -p "scripts/development" 
mkdir -p "scripts/maintenance"

# Backup et archives
mkdir -p "archive/old_readme"
mkdir -p "archive/old_scripts"

# Documentation mieux organisée  
mkdir -p "docs/assets/diagrams"
mkdir -p "docs/assets/images"
mkdir -p "docs/guides"

echo "✅ Dossiers créés"

# Déplacement des scripts de déploiement
echo "🚀 Organisation des scripts de déploiement..."
mv auto-push.sh scripts/deployment/ 2>/dev/null || true
mv store-token.sh scripts/deployment/ 2>/dev/null || true
mv github-auth.sh scripts/deployment/ 2>/dev/null || true
mv master-push.sh scripts/deployment/ 2>/dev/null || true
mv final-push.sh scripts/deployment/ 2>/dev/null || true
mv push-to-github.sh scripts/deployment/ 2>/dev/null || true
mv secure-push.sh scripts/deployment/ 2>/dev/null || true

# Scripts de développement  
echo "🔧 Organisation des scripts de développement..."
mv convert-svg-inline.sh scripts/development/ 2>/dev/null || true
mv convert-to-png.sh scripts/development/ 2>/dev/null || true
mv docs/generate_diagrams.sh scripts/development/ 2>/dev/null || true

# Scripts de maintenance
echo "🧹 Organisation des scripts de maintenance..."
mv fix-readme-github.sh scripts/maintenance/ 2>/dev/null || true
mv fix-svg-github.sh scripts/maintenance/ 2>/dev/null || true

# Archive des anciens README  
echo "📦 Archive des anciens fichiers..."
mv README_old.md archive/old_readme/ 2>/dev/null || true
mv README_clean.md archive/old_readme/ 2>/dev/null || true  
mv README_png_backup.md archive/old_readme/ 2>/dev/null || true
mv README_with_svg.md archive/old_readme/ 2>/dev/null || true
mv docs/README.md.backup archive/old_readme/ 2>/dev/null || true

# Archive fichiers de développement obsolètes
mv bot-temp.js archive/ 2>/dev/null || true
mv index-corrupted.js archive/ 2>/dev/null || true
mv test-description.js archive/ 2>/dev/null || true
mv heroku-setup.md archive/ 2>/dev/null || true

# Réorganisation des assets de documentation
echo "🎨 Réorganisation des assets de documentation..."
mv docs/images/* docs/assets/images/ 2>/dev/null || true
rmdir docs/images 2>/dev/null || true

mv docs/inline_svg/* docs/assets/diagrams/ 2>/dev/null || true
rmdir docs/inline_svg 2>/dev/null || true

# Garder aussi les SVG originaux dans diagrams
mv docs/*.svg docs/assets/diagrams/ 2>/dev/null || true
mv docs/*.dot docs/assets/diagrams/ 2>/dev/null || true

# Réorganisation des guides
mv docs/QUICK_INSTALL.md docs/guides/ 2>/dev/null || true
mv docs/FAQ.md docs/guides/ 2>/dev/null || true
mv docs/INDEX.md docs/guides/ 2>/dev/null || true
mv docs/SYNTHESIS.md docs/guides/ 2>/dev/null || true

echo "✅ Réorganisation terminée"

# Création de liens symboliques pour la compatibilité
echo "🔗 Création de liens de compatibilité..."
ln -sf scripts/deployment/auto-push.sh auto-push.sh 2>/dev/null || true
ln -sf guides/QUICK_INSTALL.md docs/QUICK_INSTALL.md 2>/dev/null || true
ln -sf guides/FAQ.md docs/FAQ.md 2>/dev/null || true
ln -sf guides/INDEX.md docs/INDEX.md 2>/dev/null || true

echo "✅ Liens créés"

echo
echo "🎉 Nettoyage terminé !"