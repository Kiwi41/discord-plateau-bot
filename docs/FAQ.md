# ❓ FAQ - Questions fréquentes

*Réponses aux questions les plus courantes sur le bot Discord Plateaux*

## 🚀 Installation et déploiement

### ❓ "J'ai un message d'erreur : 'heroku: command not found'"
**Réponse :** Tu dois installer Heroku CLI sur ton ordinateur.
- **Windows/Mac :** https://devcenter.heroku.com/articles/heroku-cli
- **Linux :** `curl https://cli-assets.heroku.com/install.sh | sh`

### ❓ "Comment créer un compte Heroku ?"
**Réponse :** Va sur https://signup.heroku.com/ et inscris-toi gratuitement. Tu n'as pas besoin de carte de crédit pour la version gratuite.

### ❓ "Où trouver mon token Discord ?"
**Réponse :** 
1. Va sur https://discord.com/developers/applications
2. Sélectionne ton application → Menu "Bot" 
3. Clique sur "Reset Token" si c'est la première fois
4. **Garde-le secret !** Ne le partage jamais.

### ❓ "Comment activer le mode développeur Discord ?"
**Réponse :** 
1. Dans Discord → Paramètres utilisateur (roue dentée)
2. "Avancé" → Active "Mode développeur"
3. Maintenant tu peux faire clic droit → "Copier l'ID" sur serveurs/canaux

---

## 🤖 Fonctionnement du bot

### ❓ "Le bot ne répond pas à mes commandes"
**Solutions possibles :**
- ✅ Vérifie qu'il est en ligne (point vert dans la liste des membres)
- ✅ Vérifie qu'il a les permissions "Envoyer des messages" 
- ✅ Essaie dans un canal où il peut écrire
- ✅ Regarde les logs : `heroku logs --tail`

### ❓ "Le bot crée des posts avec des valeurs par défaut"
**Cause :** Aucun événement Discord trouvé pour ce vendredi.
**Solutions :**
- 📅 Crée des événements Discord avec "plateau" ou "soirée" dans le nom
- 📅 Mets la date sur un vendredi 
- 🔍 Vérifie l'heure de l'événement (doit être dans le futur)

### ❓ "Quand le bot crée-t-il les posts automatiquement ?"
**Réponse :** Chaque **samedi à 3h00 du matin** (timezone configurée), il traite les 4 prochains vendredis.
**Pour changer l'heure :** Modifie la ligne `cron.schedule('0 3 * * 6', ...)` dans `index.js`

### ❓ "Le bot trouve plusieurs événements, lequel choisit-il ?"
**Réponse :** Il prend le **premier événement récurrent** qui contient les mots-clés ("plateau", "soirée", etc.) dans le nom.
**Si pas d'événement récurrent :** Il prend le premier événement unique du vendredi.

---

## 🔧 Configuration et personnalisation

### ❓ "Comment changer l'heure par défaut (20h30) ?"
**Réponse :** Dans `index.js`, cherche "valeurs par défaut" et modifie :
```javascript
eventTime = '19:00'; // Par exemple pour 19h00
```

### ❓ "Comment changer le lieu par défaut ?"
**Réponse :** Dans `index.js`, modifie :
```javascript
eventLocation = '📍 Ma nouvelle adresse';
```

### ❓ "Comment ajouter des mots-clés de recherche ?"
**Réponse :** Dans `index.js`, cherche `keywords` et ajoute :
```javascript
const keywords = ['plateau', 'soirée', 'jeu', 'board', 'game', 'nouveau_mot'];
```

### ❓ "Puis-je changer la planification automatique ?"
**Réponse :** Oui, dans `index.js` ligne ~750, change le cron :
```javascript
// Actuel : samedi 3h00
cron.schedule('0 3 * * 6', () => {

// Exemples d'autres planifications :
cron.schedule('0 10 * * 2', () => { // Mardi 10h00 (exemple de changement)
cron.schedule('0 18 * * 5', () => { // Vendredi 18h00
```

---

## 🛠️ Dépannage

### ❓ "Comment voir les logs d'erreur ?"
**Réponse :** 
```bash
heroku logs --tail          # Logs en temps réel
heroku logs -n 100          # 100 dernières lignes
heroku logs --source app    # Seulement les logs de l'app
```

### ❓ "Le bot s'est arrêté, comment le redémarrer ?"
**Réponse :**
```bash
heroku restart              # Redémarre l'app
heroku ps                   # Vérifie l'état
heroku ps:scale worker=1    # S'assure qu'1 worker tourne
```

### ❓ "Erreur : 'Missing permissions'"
**Réponse :** Le bot n'a pas les bonnes permissions Discord.
**Solution :**
1. Va dans les paramètres de ton serveur → "Rôles"
2. Trouve le rôle de ton bot
3. Active : "Envoyer des messages", "Créer des fils publics", "Intégrer des liens"

### ❓ "Erreur : 'DiscordAPIError: Unknown Channel'"
**Réponse :** L'ID du canal forum est incorrect.
**Solution :**
1. Vérifie que c'est bien un **canal forum** (pas un canal texte normal)
2. Clic droit sur le canal → "Copier l'ID"
3. Mets à jour avec `heroku config:set FORUM_CHANNEL_ID=nouvel_id`

### ❓ "Erreur : 'Timeout' lors de la récupération des événements"
**Réponse :** L'API Discord est temporairement lente.
**Solution :** Le bot a un système de retry automatique (3 tentatives). Si ça persiste :
```bash
heroku restart  # Redémarre le bot
```

---

## 💡 Fonctionnalités avancées

### ❓ "Comment fonctionne le cycle de vie du bot ?"
**Réponse :** Le bot suit un cycle précis :

![Cycle de vie](bot_lifecycle.svg)

1. **🚀 Démarrage** : Chargement config → Connexion Discord → Vérification permissions
2. **👂 Écoute** : Attente commandes utilisateur et déclencheurs cron
3. **📋 Traitement** : Récupération événements → Calcul vendredis → Actions forum
4. **🛠️ Gestion erreurs** : Retry automatique → Logging → Continuation
5. **😴 Attente** : Retour en veille jusqu'à prochaine activité

### ❓ "Que se passe-t-il exactement lors du traitement d'un vendredi ?"
**Réponse :** Processus détaillé en plusieurs étapes :

![Traitement événement](event_processing.svg)

- **API Discord** : Récupération avec 3 tentatives (2s, 4s, 6s de délai)
- **Filtrage intelligent** : Date exacte + mots-clés + priorité récurrente  
- **Extraction données** : Heure, lieu, description avec formatage timezone
- **Action forum** : Comparaison contenu → Création/Mise à jour → Logging

### ❓ "Puis-je faire tourner le bot sur mon ordinateur au lieu d'Heroku ?"
**Réponse :** Oui pour les tests, mais ton ordinateur doit rester allumé 24h/24.
```bash
npm install
node index.js
```

### ❓ "Comment sauvegarder ma configuration ?"
**Réponse :**
```bash
# Sauvegarder les variables Heroku
heroku config > config_backup.txt

# Sauvegarder le code
git clone https://github.com/ton-repo backup/
```

### ❓ "Puis-je avoir plusieurs bots sur des serveurs différents ?"
**Réponse :** Oui ! Crée une app Heroku différente pour chaque serveur avec ses propres variables d'environnement.

### ❓ "Comment modifier le message du post ?"
**Réponse :** Dans `index.js`, cherche la fonction `createForumPost()` et modifie l'embed :
```javascript
.setDescription('🎲 Mon nouveau message personnalisé !')
```

---

## 📊 Monitoring et statistiques

### ❓ "Comment savoir si le bot fonctionne bien ?"
**Réponse :** Surveille ces logs dans `heroku logs --tail` :
- ✅ `Bot connecté en tant que...`
- ✅ `événements trouvés sur le serveur`
- ✅ `Post créé:` ou `Post mis à jour:`

### ❓ "Le bot consomme-t-il beaucoup de ressources Heroku ?"
**Réponse :** Non, très peu :
- **RAM :** ~50-100 MB
- **CPU :** Quasi-nul (seulement actif quelques secondes/jour)
- **Bandwidth :** Très faible (quelques KB par jour)

### ❓ "Puis-je voir des statistiques d'utilisation ?"
**Réponse :** 
```bash
heroku logs --source app | grep "Post créé"  # Nombre de posts créés
heroku ps                                     # État des processus
```

---

## 🔒 Sécurité

### ❓ "Mon token Discord a été exposé, que faire ?"
**Réponse :** **URGENT !**
1. Va sur https://discord.com/developers/applications
2. "Bot" → "Reset Token" immédiatement  
3. Mets à jour Heroku : `heroku config:set DISCORD_TOKEN=nouveau_token`

### ❓ "Qui peut utiliser les commandes du bot ?"
**Réponse :** 
- `!create-plateau-post` et `!process-next-month` : **Admins seulement**
- `!plateau-help` : **Tout le monde**

### ❓ "Comment limiter le bot à certains canaux ?"
**Réponse :** Modifie les permissions Discord du bot pour qu'il ne puisse écrire que dans certains canaux.

---

## 💰 Coûts

### ❓ "Heroku est-il vraiment gratuit ?"
**Réponse :** Heroku a supprimé son offre gratuite. Tu as besoin du plan "Eco" à ~5$/mois pour faire tourner ton bot 24h/24.

### ❓ "Existe-t-il des alternatives gratuites à Heroku ?"
**Réponse :** Oui :
- **Railway.app** : 5$ de crédit gratuit/mois
- **Render.com** : Plan gratuit avec limitations  
- **Fly.io** : Généreuse offre gratuite
- **VPS** : DigitalOcean, Linode (~5$/mois)

### ❓ "Puis-je héberger gratuitement chez moi ?"
**Réponse :** Oui avec un Raspberry Pi ou ordinateur qui reste allumé, mais :
- ⚠️ Connexion internet stable requise
- ⚠️ Pas de support technique
- ⚠️ Coupures possibles

---

## 📞 Support

### ❓ "Où trouver plus d'aide ?"
**Réponse :**
1. **Documentation complète** : [README.md](README.md)
2. **Guide rapide** : [QUICK_INSTALL.md](QUICK_INSTALL.md)  
3. **Discord.js docs** : https://discord.js.org/
4. **Heroku docs** : https://devcenter.heroku.com/

### ❓ "Comment signaler un bug ?"
**Réponse :** Prépare ces informations :
- Version du bot (`package.json`)
- Logs d'erreur complets (`heroku logs`)
- Étapes pour reproduire le problème
- Configuration (sans les tokens secrets !)

---

*FAQ mise à jour le 8 octobre 2025*