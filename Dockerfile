FROM node:18-bullseye-slim

# Créer un utilisateur non-root pour la sécurité
RUN useradd --user-group --create-home --shell /bin/false appuser

WORKDIR /usr/src/app

# Copier package.json et package-lock.json si présent pour profiter du cache Docker
COPY package.json package-lock.json* ./

# Installer seulement les dépendances de production
RUN npm ci --only=production --no-audit --no-fund

# Copier le reste du code
COPY . .

# Donner la propriété des fichiers à l'utilisateur non-root
RUN chown -R appuser:appuser /usr/src/app

USER appuser

ENV NODE_ENV=production

# Exposer un port informatif (le bot n'écoute pas de port HTTP par défaut)
EXPOSE 3000

CMD ["node", "index.js"]
