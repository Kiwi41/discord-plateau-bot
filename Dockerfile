# Utiliser une image Python officielle
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les locales françaises
RUN apt-get update && \
    apt-get install -y locales && \
    sed -i '/fr_FR.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Définir les variables d'environnement pour les locales
ENV LANG=fr_FR.UTF-8
ENV LANGUAGE=fr_FR:fr
ENV LC_ALL=fr_FR.UTF-8

# Copier le fichier des dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code du bot
COPY bot.py .
COPY stats_manager.py .

# Créer un utilisateur non-root pour exécuter le bot
RUN useradd -m -u 1000 botuser && \
    chown -R botuser:botuser /app

USER botuser

# Commande pour lancer le bot
CMD ["python", "-u", "bot.py"]
