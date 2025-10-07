# Discord Bot pour Soirées Plateaux

Ce projet contient un bot Discord qui crée automatiquement des posts dans un forum pour planifier les soirées plateaux du vendredi soir.

## Fonctionnalités
- Création automatique de posts hebdomadaires chaque mardi à 10h
- Intégration avec les forums Discord  
- Planification des événements récurrents avec node-cron
- Messages avec embeds Discord élégants
- Liens d'inscription automatiques
- Commande administrative pour création manuelle
- Support des fuseaux horaires

## Configuration requise
Le bot nécessite:
- Node.js (version 18+) installé sur le système
- Token Discord Bot depuis le Developer Portal
- ID du serveur Discord (Guild ID)  
- ID du canal forum planning-plateau
- URL d'inscription pour les événements
- Configuration des variables d'environnement dans un fichier .env

## Technologies utilisées
- Node.js avec discord.js v14
- node-cron pour la planification automatique
- dotenv pour la gestion des variables d'environnement
- EmbedBuilder pour les messages enrichis

## Prochaines étapes
1. Installer Node.js sur le système
2. Configurer les variables d'environnement (.env)
3. Obtenir les IDs Discord nécessaires  
4. Tester le bot et ajuster les paramètres