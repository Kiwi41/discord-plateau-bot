#!/bin/bash

echo "🔄 Conversion des SVG avec CSS vers SVG inline GitHub-compatible"
echo

# Fonction pour convertir un SVG Graphviz en SVG inline
convert_graphviz_to_inline() {
    local input_file="$1"
    local output_file="$2"
    
    echo "🔧 Conversion: $input_file → $output_file"
    
    # Lire le SVG d'origine et remplacer les classes par des styles inline
    sed -e '/<style>/,/<\/style>/d' \
        -e 's/class="title"/font="bold 16px sans-serif" text-anchor="middle"/g' \
        -e 's/class="label"/font="12px sans-serif" text-anchor="middle"/g' \
        -e 's/class="box"/fill="#e3f2fd" stroke="#1976d2" stroke-width="2" rx="8"/g' \
        -e 's/class="cloud"/fill="#fff3e0" stroke="#f57c00" stroke-width="2" rx="12"/g' \
        -e 's/class="bot"/fill="#e8f5e8" stroke="#388e3c" stroke-width="2" rx="8"/g' \
        -e 's/class="arrow"/stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/g' \
        -e 's/class="process"/fill="#e3f2fd" stroke="#1976d2" stroke-width="2" rx="8"/g' \
        -e 's/class="decision"/fill="#fff3e0" stroke="#f57c00" stroke-width="2"/g' \
        -e 's/class="action"/fill="#e8f5e8" stroke="#388e3c" stroke-width="2" rx="8"/g' \
        -e 's/class="error"/fill="#ffebee" stroke="#f44336" stroke-width="2" rx="8"/g' \
        -e 's/class="sleep"/fill="#f5f5f5" stroke="#9e9e9e" stroke-width="2" rx="8"/g' \
        -e 's/class="start"/fill="#4caf50" stroke="#388e3c" stroke-width="2"/g' \
        -e 's/class="small"/font="9px sans-serif" text-anchor="middle"/g' \
        "$input_file" > "$output_file"
    
    echo "   ✅ Converti avec succès"
}

cd "/home/a154355/git/perso/Discord/docs"

# Liste des fichiers à convertir
svg_files=(
    "architecture.svg"
    "bot_lifecycle.svg" 
    "data_flow.svg"
    "deployment.svg"
    "event_processing.svg"
    "user_workflow.svg"
    "simple_architecture.svg"
    "simple_lifecycle.svg"
    "simple_workflow.svg"
)

# Créer le dossier pour les versions inline
mkdir -p "inline_svg"

for svg_file in "${svg_files[@]}"; do
    if [ -f "$svg_file" ]; then
        output_file="inline_svg/${svg_file}"
        convert_graphviz_to_inline "$svg_file" "$output_file"
        
        # Vérifier la taille
        original_size=$(du -h "$svg_file" | cut -f1)
        inline_size=$(du -h "$output_file" | cut -f1)
        echo "   📏 Taille: $original_size → $inline_size"
    else
        echo "⚠️ Fichier non trouvé: $svg_file"
    fi
    echo
done

echo "🎉 Conversion terminée !"
echo "📂 Les SVG inline sont dans docs/inline_svg/"
echo "📋 Ces SVG fonctionnent sur GitHub sans problème de CSS"