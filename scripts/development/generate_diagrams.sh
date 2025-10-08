#!/bin/bash

# 🎨 Script de génération des diagrammes Graphviz
# Génère automatiquement tous les diagrammes SVG depuis les fichiers .dot

echo "🎨 Génération des diagrammes de documentation..."
echo

# Vérifier que Graphviz est installé
if ! command -v dot &> /dev/null; then
    echo "❌ Erreur : Graphviz (dot) n'est pas installé."
    echo "   Installation : sudo apt install graphviz"
    exit 1
fi

# Se placer dans le dossier docs
cd "$(dirname "$0")" || exit 1

# Compteurs
generated=0
errors=0

# Fonction pour générer un diagramme
generate_diagram() {
    local dot_file="$1"
    local svg_file="${dot_file%.dot}.svg"
    
    echo -n "📊 Génération de $svg_file... "
    
    if dot -Tsvg "$dot_file" -o "$svg_file" 2>/dev/null; then
        echo "✅ OK"
        ((generated++))
    else
        echo "❌ ERREUR"
        ((errors++))
    fi
}

# Générer tous les diagrammes
for dot_file in *.dot; do
    if [ -f "$dot_file" ]; then
        generate_diagram "$dot_file"
    fi
done

echo
echo "📈 Résumé :"
echo "   ✅ Diagrammes générés : $generated"
echo "   ❌ Erreurs : $errors"

if [ $errors -eq 0 ]; then
    echo "   🎉 Tous les diagrammes ont été générés avec succès !"
else
    echo "   ⚠️  Certains diagrammes n'ont pas pu être générés."
    exit 1
fi

# Afficher la taille des fichiers générés
echo
echo "📁 Fichiers générés :"
for svg_file in *.svg; do
    if [ -f "$svg_file" ]; then
        size=$(du -h "$svg_file" | cut -f1)
        echo "   📊 $svg_file ($size)"
    fi
done

echo
echo "✨ Génération terminée !"