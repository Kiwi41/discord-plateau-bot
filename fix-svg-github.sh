#!/bin/bash

echo "🔄 Conversion des SVG pour GitHub"
echo

# Répertoire des diagrammes
DIAGRAMS_DIR="/home/a154355/git/perso/Discord/docs/diagrams"

# Fonction pour convertir un SVG en version GitHub-compatible
convert_svg_for_github() {
    local svg_file="$1"
    local filename=$(basename "$svg_file" .svg)
    local output_file="${DIAGRAMS_DIR}/${filename}_github.svg"
    
    echo "🔧 Conversion de $filename.svg..."
    
    # Lire le fichier SVG et remplacer les styles CSS par des attributs inline
    sed '/<style>/,/<\/style>/d' "$svg_file" > "$output_file.tmp"
    
    # Remplacer les classes par des styles inline
    sed -i 's/class="title"/style="font: bold 16px sans-serif; text-anchor: middle;"/g' "$output_file.tmp"
    sed -i 's/class="label"/style="font: 12px sans-serif; text-anchor: middle;"/g' "$output_file.tmp"
    sed -i 's/class="box"/style="fill: #e3f2fd; stroke: #1976d2; stroke-width: 2; rx: 8;"/g' "$output_file.tmp"
    sed -i 's/class="cloud"/style="fill: #fff3e0; stroke: #f57c00; stroke-width: 2; rx: 12;"/g' "$output_file.tmp"
    sed -i 's/class="bot"/style="fill: #e8f5e8; stroke: #388e3c; stroke-width: 2; rx: 8;"/g' "$output_file.tmp"
    sed -i 's/class="arrow"/style="stroke: #666; stroke-width: 2; marker-end: url(#arrowhead);"/g' "$output_file.tmp"
    
    mv "$output_file.tmp" "$output_file"
    echo "   ✅ Créé: ${filename}_github.svg"
}

# Convertir tous les SVG
for svg_file in "$DIAGRAMS_DIR"/*.svg; do
    if [[ "$svg_file" != *"_github.svg" ]]; then
        convert_svg_for_github "$svg_file"
    fi
done

echo
echo "📝 Mise à jour du README avec les nouveaux SVG..."

# Backup du README original
cp "/home/a154355/git/perso/Discord/docs/README.md" "/home/a154355/git/perso/Discord/docs/README.md.backup"

# Remplacer les références SVG dans le README
sed -i 's/diagrams\/architecture\.svg/diagrams\/architecture_github.svg/g' "/home/a154355/git/perso/Discord/docs/README.md"
sed -i 's/diagrams\/data_flow\.svg/diagrams\/data_flow_github.svg/g' "/home/a154355/git/perso/Discord/docs/README.md"
sed -i 's/diagrams\/deployment\.svg/diagrams\/deployment_github.svg/g' "/home/a154355/git/perso/Discord/docs/README.md"
sed -i 's/diagrams\/user_workflow\.svg/diagrams\/user_workflow_github.svg/g' "/home/a154355/git/perso/Discord/docs/README.md"
sed -i 's/diagrams\/bot_lifecycle\.svg/diagrams\/bot_lifecycle_github.svg/g' "/home/a154355/git/perso/Discord/docs/README.md"
sed -i 's/diagrams\/event_processing\.svg/diagrams\/event_processing_github.svg/g' "/home/a154355/git/perso/Discord/docs/README.md"

echo "✅ README mis à jour avec les SVG GitHub-compatibles"
echo
echo "🚀 Push des changements vers GitHub..."