# 📁 Structure du Projet - Bot Discord Plateaux

## 🗂️ Arborescence organisée

```
discord-plateau-bot/
├── 📋 README.md              # Documentation principale
├── 🤖 index.js              # Code principal du bot
├── ⚙️  config.js             # Configuration du bot
├── 📦 package.json           # Dépendances Node.js
├── 🔧 .env.example          # Template variables d'environnement
├── 🚀 Procfile              # Configuration Heroku
│
├── 📁 scripts/              # 🔧 Scripts d'automatisation
│   ├── deployment/          # Scripts de déploiement
│   │   ├── auto-push.sh     # Push automatique GitHub
│   │   ├── store-token.sh   # Gestion token GitHub
│   │   └── github-auth.sh   # Authentification GitHub
│   ├── development/         # Scripts de développement  
│   │   ├── convert-svg-inline.sh  # Conversion SVG
│   │   ├── convert-to-png.sh      # Génération PNG
│   │   └── generate_diagrams.sh   # Génération diagrammes
│   └── maintenance/         # Scripts de maintenance
│       ├── fix-readme-github.sh   # Corrections README
│       └── fix-svg-github.sh      # Corrections SVG
│
├── 📁 docs/                 # 📚 Documentation complète
│   ├── README.md            # Guide détaillé
│   ├── assets/              # Assets de documentation
│   │   ├── images/          # Images PNG
│   │   └── diagrams/        # Diagrammes SVG & DOT
│   └── guides/              # Guides spécialisés
│       ├── QUICK_INSTALL.md # Installation rapide
│       ├── FAQ.md           # Questions fréquentes
│       ├── INDEX.md         # Index général
│       └── SYNTHESIS.md     # Synthèse technique
│
└── 📁 archive/              # 🗃️ Fichiers archivés
    ├── old_readme/          # Anciennes versions README
    ├── old_scripts/         # Scripts obsolètes
    └── *.js                 # Fichiers de développement
```

## 🎯 Scripts principaux

### 🚀 Déploiement rapide
```bash
# Push automatique vers GitHub (recommandé)
./auto-push.sh

# Ou via le lien symbolique
./scripts/deployment/auto-push.sh
```

### 🔧 Développement
```bash
# Régénérer tous les diagrammes
./scripts/development/generate_diagrams.sh

# Convertir SVG pour GitHub
./scripts/development/convert-svg-inline.sh

# Générer les PNG de backup
./scripts/development/convert-to-png.sh
```

### 🧹 Maintenance
```bash
# Corriger les README si problème
./scripts/maintenance/fix-readme-github.sh

# Corriger les SVG si problème  
./scripts/maintenance/fix-svg-github.sh
```

## 📋 Liens de compatibilité

Des liens symboliques maintiennent la compatibilité avec l'ancienne structure :
- `auto-push.sh` → `scripts/deployment/auto-push.sh`
- `docs/FAQ.md` → `docs/guides/FAQ.md`
- `docs/QUICK_INSTALL.md` → `docs/guides/QUICK_INSTALL.md`

## 🎨 Assets de documentation

### Images PNG (pour GitHub)
- `docs/assets/images/` - Versions PNG haute qualité
- Rendu garanti sur toutes les plateformes

### Diagrammes SVG (interactifs)
- `docs/assets/diagrams/` - SVG avec styles inline
- Sources DOT pour Graphviz incluses

## 🗃️ Archive

Tous les anciens fichiers sont conservés dans `archive/` :
- Anciennes versions de README
- Scripts de développement obsolètes  
- Fichiers de test et temporaires

## 🔄 Migration depuis l'ancienne structure

Si vous avez cloné une version antérieure :

```bash
# Réorganiser automatiquement
./reorganize-project.sh

# Ou manuellement :
git pull origin main
# Les nouveaux chemins sont automatiquement utilisés
```

## 💡 Bonnes pratiques

### 📝 Documentation
- README principal : vue d'ensemble et démarrage rapide
- `docs/README.md` : documentation technique complète
- `docs/guides/` : guides spécialisés par sujet

### 🔧 Scripts
- Utilisez `auto-push.sh` pour tous les commits
- Scripts de développement dans `scripts/development/`
- Ne jamais modifier directement les assets générés

### 🎨 Assets
- Images PNG pour compatibilité maximale
- SVG inline pour interactivité GitHub
- Sources DOT conservées pour modifications futures

---

Cette structure rend le projet plus **professionnel**, **maintenable** et **facile à naviguer** ! 🚀