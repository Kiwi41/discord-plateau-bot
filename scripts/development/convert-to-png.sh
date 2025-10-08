#!/bin/bash

echo "🖼️ Conversion des diagrammes SVG vers PNG pour GitHub"
echo

# Créer le dossier pour les images PNG
mkdir -p "/home/a154355/git/perso/Discord/docs/images"

# Liste des diagrammes à convertir
diagrams=(
    "architecture"
    "bot_lifecycle"
    "data_flow"
    "deployment"
    "event_processing"
    "user_workflow"
    "simple_architecture"
    "simple_lifecycle"
    "simple_workflow"
)

cd "/home/a154355/git/perso/Discord/docs"

for diagram in "${diagrams[@]}"; do
    svg_file="${diagram}.svg"
    png_file="images/${diagram}.png"
    
    if [ -f "$svg_file" ]; then
        echo "🔄 Conversion: $svg_file → $png_file"
        
        # Conversion avec rsvg-convert (meilleure qualité)
        rsvg-convert -w 800 -h 600 -f png "$svg_file" -o "$png_file"
        
        if [ $? -eq 0 ]; then
            echo "   ✅ Succès: $png_file créé"
            # Vérifier la taille du fichier
            size=$(du -h "$png_file" | cut -f1)
            echo "   📏 Taille: $size"
        else
            echo "   ❌ Erreur lors de la conversion de $svg_file"
        fi
    else
        echo "⚠️ Fichier non trouvé: $svg_file"
    fi
    echo
done

echo "📊 Résumé des conversions:"
echo "📁 Dossier PNG: docs/images/"
ls -la "/home/a154355/git/perso/Discord/docs/images/" | grep "\.png$" | wc -l | xargs echo "🖼️ Nombre de PNG créés:"

echo
echo "🎨 Création d'un diagramme simple pour le README principal..."

# Créer un diagramme simple avec ImageMagick pour le README principal
cat > "/tmp/create_main_diagram.sh" << 'EOF'
#!/bin/bash
convert -size 800x400 xc:white \
    -fill '#e3f2fd' -stroke '#1976d2' -strokewidth 2 \
    -draw "roundrectangle 50,50 200,150 10,10" \
    -fill black -pointsize 14 -gravity center \
    -draw "text -250,0 '🎮 Discord'" \
    -draw "text -250,20 'Serveur & Forum'" \
    \
    -fill '#fff3e0' -stroke '#f57c00' -strokewidth 2 \
    -draw "roundrectangle 300,50 450,150 10,10" \
    -fill black -pointsize 14 -gravity center \
    -draw "text 0,0 '☁️ Heroku'" \
    -draw "text 0,20 'Bot Node.js'" \
    \
    -fill '#e8f5e8' -stroke '#388e3c' -strokewidth 2 \
    -draw "roundrectangle 550,50 700,150 10,10" \
    -fill black -pointsize 14 -gravity center \
    -draw "text 250,0 '👥 Communauté'" \
    -draw "text 250,20 'Posts & Events'" \
    \
    -stroke '#666' -strokewidth 3 \
    -draw "line 200,100 300,100" \
    -draw "line 450,100 550,100" \
    \
    -fill black -pointsize 16 -gravity north \
    -draw "text 0,20 '🎲 Bot Discord - Soirées Plateaux'" \
    \
    -fill black -pointsize 12 -gravity south \
    -draw "text 0,40 'Automatisation: Samedi 3h → Crée posts pour 4 vendredis'" \
    \
    /home/a154355/git/perso/Discord/docs/images/main_overview.png
EOF

chmod +x /tmp/create_main_diagram.sh
/tmp/create_main_diagram.sh

if [ -f "/home/a154355/git/perso/Discord/docs/images/main_overview.png" ]; then
    echo "✅ Diagramme principal créé: docs/images/main_overview.png"
else
    echo "⚠️ Création du diagramme principal échouée, création d'une version simple..."
    # Version de fallback avec convert simple
    convert -size 600x200 xc:'#f8f9fa' \
        -fill black -pointsize 18 -gravity center \
        -annotate +0-60 '🎲 Bot Discord Soirées Plateaux' \
        -pointsize 14 \
        -annotate +0-30 '🎮 Discord ←→ ☁️ Heroku ←→ 👥 Communauté' \
        -pointsize 12 \
        -annotate +0+10 'Automatisation: Samedi 3h → Posts pour 4 vendredis' \
        -annotate +0+30 'GitHub: https://github.com/Kiwi41/discord-plateau-bot' \
        "/home/a154355/git/perso/Discord/docs/images/main_overview.png"
    echo "✅ Diagramme de fallback créé"
fi

echo
echo "🎉 Conversion terminée !"
echo "📂 Les images PNG sont disponibles dans docs/images/"