# Déploiement Docker sur NAS Synology

Ce guide explique comment exécuter le bot `discord-plateau-bot` dans un conteneur Docker sur un NAS Synology (via Container Manager) ou en local avec `docker-compose`.

## Résumé

- Fichiers ajoutés : `Dockerfile`, `docker-compose.yml`, `.env.example`
- Objectif : remplacer Heroku par un conteneur Docker autonome (idéal pour NAS Synology)

## Pré-requis

- NAS Synology avec Container Manager (ou Docker) installé
- Accès SSH/Terminal pour build local (optionnel)
- Variables d'environnement prêtes (voir `.env.example`)

## Construire l'image localement (optionnel)

Sur votre machine de développement (ou sur le NAS si vous avez les outils) :

```bash
# Depuis la racine du projet
docker build -t discord-plateau-bot:latest .
```

Si vous ne pouvez pas builder sur le NAS, vous pouvez builder localement et pousser l'image vers un registry privé (Docker Hub, GitHub Packages, GitLab, ou registry local) puis la déployer sur le NAS.

Pousser sur Docker Hub (exemple) :

```bash
docker tag discord-plateau-bot:latest your-dockerhub-user/discord-plateau-bot:latest
docker push your-dockerhub-user/discord-plateau-bot:latest
```

## Déployer avec Container Manager (interface graphique Synology)

1. Ouvrez "Container Manager" (ou "Docker") sur votre NAS.
2. Si vous avez une image dans Docker Hub : utilisez "Registry" -> recherchez `your-dockerhub-user/discord-plateau-bot` et téléchargez l'image.
3. Si vous préférez builder localement sur le NAS : utilisez "Image" -> "Build" (sélectionnez le Dockerfile dans le dossier partagé contenant le projet).
4. Créez un conteneur avec l'image téléchargée.

Paramètres importants à configurer dans l'interface :

- Environment : fournissez les variables listées dans `.env.example` (`DISCORD_TOKEN`, `GUILD_ID`, `FORUM_CHANNEL_ID`, etc.).
- Restart Policy : `Unless-stopped` (recommandé) ou `Always`.
- Volumes (optionnel) : montez un dossier pour logs si vous souhaitez persistance (ex : `/volume1/docker/discord-plateau-bot/logs:/usr/src/app/data`).
- Ports : normalement non nécessaires (le bot ne sert pas d'API HTTP), laissez vide.

Lancez le conteneur.

## Déployer avec docker-compose (sur un serveur ou machine Linux)

1. Copier `docker-compose.yml` et `.env` dans le dossier.
2. Lancer :

```bash
docker compose up -d --build
```

3. Vérifier les logs :

```bash
docker compose logs -f
```

## Conseils spécifiques Synology

- Si votre NAS n'a pas Docker CLI, utilisez l'interface Container Manager pour configurer l'image et les variables d'environnement.
- Pour builder directement à partir du partage réseau, assurez-vous que le dossier du projet est monté sur le NAS et accessible à l'interface Container Manager.
- Préférez l'usage d'un registry (Docker Hub privé ou GitHub Container Registry) si vous souhaitez CI/CD.

## Sécurité et maintenance

- Ne commitez jamais votre `.env` contenant `DISCORD_TOKEN` dans le dépôt.
- Si vous devez régénérer le token Discord, mettez à jour la variable d'environnement du conteneur et redémarrez le conteneur.
- Gardez Node et dépendances à jour ; reconstruisez l'image périodiquement.

## Vérifications post-déploiement

- Le bot doit se connecter automatiquement si le token est correct (vérifiez les logs du conteneur pour un message de connexion).
- Testez une commande (ex : `!create-plateau-post`) dans Discord pour vérifier la création du post.

## Dépannage rapide

- Erreur "Variables d'environnement manquantes" : vérifiez que `DISCORD_TOKEN`, `GUILD_ID` et `FORUM_CHANNEL_ID` sont définis.
- Token invalide : révoquez et générez un nouveau token dans le Developer Portal.
- Permissions : vérifiez que le bot a les permissions pour poster dans le forum.

---

Si vous le souhaitez, je peux :
- Ajouter une entrée courte dans `README.md` qui renvoie à ce guide.
- Pousser ces fichiers dans une nouvelle branche et ouvrir une PR.
