# 🚀 Guide d'installation rapide - Bot Discord Plateaux

*Installation en 15 minutes pour débutants complets*

## ✅ Checklist avant de commencer

- [ ] Compte Discord avec un serveur
- [ ] Compte Heroku (gratuit) - https://heroku.com
- [ ] Ordinateur avec connexion internet

## 🎯 Étapes simplifiées

### 1️⃣ Créer le bot Discord (5 minutes)

1. **Va sur** : https://discord.com/developers/applications
2. **Clique** : "New Application" → Nom : "Bot Plateaux"
3. **Menu gauche** : "Bot" → "Add Bot" 
4. **IMPORTANT** : Copie le **Token** et garde-le secret ! ⚠️
5. **Menu gauche** : "OAuth2" → "URL Generator"
   - Coche : `bot`
   - Coche : `Send Messages`, `Create Public Threads`, `Embed Links`
6. **Copie l'URL générée** et ouvre-la → Sélectionne ton serveur

### 2️⃣ Récupérer les identifiants Discord (3 minutes)

1. **Dans Discord** : Paramètres → Avancé → Active "Mode développeur"
2. **Clic droit sur ton serveur** → "Copier l'ID" = `GUILD_ID`
3. **Clic droit sur ton canal forum** → "Copier l'ID" = `FORUM_CHANNEL_ID`

### 3️⃣ Déployer sur Heroku (5 minutes)

1. **Télécharge le code** : [Lien vers le repository]
2. **Crée l'app Heroku** :
   ```bash
   heroku create mon-bot-plateaux
   ```

3. **Configure les variables** (remplace par tes vraies valeurs) :
   ```bash
   heroku config:set DISCORD_TOKEN=TON_TOKEN_ICI
   heroku config:set GUILD_ID=TON_GUILD_ID_ICI  
   heroku config:set FORUM_CHANNEL_ID=TON_FORUM_ID_ICI
   heroku config:set REGISTRATION_URL=https://ton-lien-inscription.com
   ```

4. **Déploie** :
   ```bash
   git push heroku master
   heroku ps:scale worker=1
   ```

### 4️⃣ Tester (2 minutes)

1. **Dans Discord**, tape : `!create-plateau-post`
2. **Vérifie** qu'un post apparaît dans ton forum
3. **Regarde les logs** : `heroku logs --tail`

## ✅ C'est terminé !

Ton bot fonctionne maintenant 24h/24 et créera automatiquement les posts chaque samedi à 3h du matin.

## 🆘 Problème ?

**Bot ne répond pas** → Vérifie qu'il a les bonnes permissions dans ton serveur  
**Erreur de token** → Révérfie que le token est correct dans Heroku  
**Pas de post créé** → Crée des événements Discord avec "plateau" dans le nom

**Logs détaillés** : `heroku logs --tail`

## 📋 Variables d'environnement complètes

```bash
# OBLIGATOIRES
DISCORD_TOKEN=ton_token_bot_discord
GUILD_ID=id_de_ton_serveur_discord
FORUM_CHANNEL_ID=id_de_ton_canal_forum
REGISTRATION_URL=https://lien-vers-inscription

# OPTIONNELLES  
TIMEZONE=Europe/Paris
EVENT_ID=id_evenement_recurrent (si tu en as un)
```

## 🎮 Commandes du bot

- `!create-plateau-post` - Créer un post pour vendredi prochain
- `!process-next-month` - Créer 4 posts pour les 4 prochains vendredis
- `!plateau-help` - Aide

---

**🎉 Amuse-toi bien avec tes soirées plateaux !**

*Pour plus de détails → [Documentation complète](README.md)*