# 📊 Système de Statistiques - Discord Bot Soirées Plateaux

## Vue d'ensemble

Le bot collecte automatiquement les statistiques de participation à chaque soirée et offre des analyses détaillées pour suivre l'évolution de votre communauté.

## Fonctionnalités principales

### 📈 Collecte automatique
- **Déclencheur** : À chaque mise à jour de la liste des participant·e·s (toutes les 15 min)
- **Données enregistrées** : Date, nom de l'événement, liste complète des participant·e·s, ID Discord
- **Persistance** : Fichier `stats.json` conservé entre les redémarrages

### 📊 Analyses disponibles
- Nombre total d'événements organisés
- Participant·e·s uniques (nombre total de personnes différentes)
- Moyenne de participation par soirée
- Top 10 des participant·e·s les plus régulier·e·s
- Tendances sur les 6 derniers mois
- Historique des 5 dernières soirées

### 👤 Statistiques individuelles
- Nombre total de participations
- Date de première participation
- Liste des 5 dernières participations

## Commandes

### Statistiques générales
```
!stats
```

Affiche un embed complet avec :
- 🎲 Nombre total d'événements
- 👥 Nombre de participant·e·s uniques
- 📈 Moyenne de participation
- 🏆 Top 5 des participant·e·s
- 📊 Tendance des 3 derniers mois
- 📅 3 dernières soirées avec leur participation

**Exemple d'affichage** :
```
📊 Statistiques des Soirées Plateaux
Vue d'ensemble de nos soirées jeux

🎲 Événements
Total: 24 soirées organisées

👥 Participant·e·s uniques
Total: 18

📈 Moyenne de participation
8.5 personnes par soirée

🏆 Top 5 des participant·e·s
🥇 Alice - 22 soirées
🥈 Bob - 19 soirées
🥉 Charlie - 17 soirées
4️⃣ David - 15 soirées
5️⃣ Emma - 14 soirées

📊 Tendance récente
2024-10: 4 soirées, 9.2 personnes en moyenne
2024-11: 4 soirées, 8.5 personnes en moyenne
2024-12: 3 soirées, 7.3 personnes en moyenne

📅 Dernières soirées
2024-12-20 - 8 participant·e·s
2024-12-13 - 7 participant·e·s
2024-12-06 - 7 participant·e·s

Première soirée enregistrée: 2024-06-07
```

### Statistiques d'un·e participant·e
```
!stats Alice
```

Affiche :
- 📈 Nombre total de participations
- 📅 Date de première participation
- 🗓️ Liste des 5 dernières participations

**Exemple d'affichage** :
```
📊 Statistiques de Alice

📈 Participations
Total: 22 soirées

📅 Première participation
2024-06-07T00:00:00+02:00

🗓️ Dernières participations
2024-12-20T00:00:00+01:00
2024-12-13T00:00:00+01:00
2024-12-06T00:00:00+01:00
2024-11-29T00:00:00+01:00
2024-11-22T00:00:00+01:00
```

## Structure des données

### Fichier `stats.json`

```json
{
  "events": [
    {
      "date": "2024-12-20T00:00:00+01:00",
      "name": "Soirée Plateaux - Vendredi 20 décembre 2024",
      "participants": ["Alice", "Bob", "Charlie", ...],
      "participant_count": 8,
      "event_id": "1234567890123456789",
      "created_at": "2024-12-14T10:30:00+01:00",
      "updated_at": "2024-12-20T20:15:00+01:00"  // Si mis à jour
    }
  ],
  "participants": {
    "Alice": {
      "total_events": 22,
      "events_attended": ["2024-06-07T00:00:00+02:00", ...],
      "first_attendance": "2024-06-07T00:00:00+02:00"
    }
  },
  "metadata": {
    "first_event": "2024-06-07T00:00:00+02:00",
    "last_updated": "2024-12-20T21:45:00+01:00"
  }
}
```

### Événement enregistré
- `date` : Date ISO de l'événement (avec timezone)
- `name` : Nom complet de l'événement
- `participants` : Liste des noms des participant·e·s
- `participant_count` : Nombre total de participant·e·s
- `event_id` : ID Discord de l'événement (nullable)
- `created_at` : Date de création de l'enregistrement
- `updated_at` : Date de dernière mise à jour (si modifié)

### Participant·e enregistré·e
- `total_events` : Nombre total de participations
- `events_attended` : Liste des dates de participation (ISO)
- `first_attendance` : Date de première participation

### Métadonnées
- `first_event` : Date du premier événement enregistré
- `last_updated` : Timestamp de dernière modification du fichier

## Gestion du fichier stats.json

### ⚠️ Importantes recommandations

1. **Ne jamais supprimer** `stats.json` : Contient tout l'historique
2. **Sauvegardes régulières** : Copier le fichier avant chaque mise à jour majeure
3. **Lecture seule** : Ne pas modifier manuellement (risque de corruption)
4. **Ajout au .gitignore** : Le fichier est exclu du dépôt Git

### 💾 Persistance avec Docker

Pour conserver les statistiques entre les redémarrages du conteneur :

**Option 1 : docker-compose.yml avec volume**
```yaml
services:
  discord-bot:
    # ... autres paramètres ...
    volumes:
      - ./stats.json:/app/stats.json
```

**Option 2 : docker run avec bind mount**
```bash
docker run -d \
  -v $(pwd)/stats.json:/app/stats.json \
  # ... autres paramètres ...
  ghcr.io/kiwi41/discord-plateau-bot:latest
```

**Option 3 : Créer le fichier avant le premier lancement**
```bash
# Créer un fichier vide
echo '{"events":[],"participants":{},"metadata":{"first_event":null,"last_updated":null}}' > stats.json

# Définir les bonnes permissions
chmod 666 stats.json

# Lancer le conteneur avec le volume
docker compose up -d
```

### 🔧 Maintenance

#### Réinitialiser les statistiques
```bash
# Sauvegarder l'ancien fichier
mv stats.json stats.backup.$(date +%Y%m%d).json

# Le bot créera un nouveau fichier au prochain événement
docker compose restart
```

#### Fusionner des statistiques
Si vous avez plusieurs fichiers stats et souhaitez les fusionner :
```python
import json

def merge_stats(file1, file2, output):
    with open(file1) as f1, open(file2) as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)
    
    # Fusionner les événements (éviter les doublons par date+name)
    events = {(e['date'], e['name']): e for e in data1['events'] + data2['events']}
    
    # Fusionner les participants
    participants = {}
    for name in set(list(data1['participants'].keys()) + list(data2['participants'].keys())):
        p1 = data1['participants'].get(name, {})
        p2 = data2['participants'].get(name, {})
        
        participants[name] = {
            'total_events': p1.get('total_events', 0) + p2.get('total_events', 0),
            'events_attended': sorted(set(
                p1.get('events_attended', []) + 
                p2.get('events_attended', [])
            )),
            'first_attendance': min([
                p1.get('first_attendance'), 
                p2.get('first_attendance')
            ] if p1.get('first_attendance') and p2.get('first_attendance') else 
              [p1.get('first_attendance') or p2.get('first_attendance')])
        }
    
    merged = {
        'events': list(events.values()),
        'participants': participants,
        'metadata': {
            'first_event': min(filter(None, [
                data1['metadata'].get('first_event'),
                data2['metadata'].get('first_event')
            ])),
            'last_updated': max([
                data1['metadata'].get('last_updated', ''),
                data2['metadata'].get('last_updated', '')
            ])
        }
    }
    
    with open(output, 'w') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)

merge_stats('stats1.json', 'stats2.json', 'stats_merged.json')
```

## Architecture technique

### Classe StatsManager

**Fichier** : `stats_manager.py`

**Méthodes principales** :

```python
# Enregistrer un événement
stats_manager.record_event(
    event_date="2024-12-20T00:00:00+01:00",
    event_name="Soirée Plateaux - Vendredi 20 décembre 2024",
    participants=["Alice", "Bob", "Charlie"],
    event_id="1234567890123456789"
)

# Obtenir les statistiques complètes
stats = stats_manager.export_stats()

# Statistiques spécifiques
total = stats_manager.get_total_events()
avg = stats_manager.get_average_participants()
top = stats_manager.get_top_participants(limit=10)
trend = stats_manager.get_participation_trend(months=6)

# Stats d'un·e participant·e
participant_stats = stats_manager.get_participant_stats("Alice")
```

### Intégration dans bot.py

Les statistiques sont enregistrées automatiquement dans la fonction `update_post_participants()` :

```python
# Après mise à jour réussie des participants
if participant_list:
    stats_manager.record_event(
        event_date=friday_date.isoformat(),
        event_name=f"Soirée Plateaux - {format_date(friday_date)}",
        participants=[p.strip() for p in participant_list],
        event_id=str(event.id) if event else None
    )
```

## Cas d'usage

### Analyser l'engagement de la communauté
```
!stats
```
→ Vérifier la moyenne de participation et la tendance

### Identifier les membres actifs
```
!stats
```
→ Consulter le Top 5 des participant·e·s

### Suivre la participation d'une personne
```
!stats Alice
```
→ Voir l'historique complet

### Détecter des baisses de participation
```
!stats
```
→ Analyser la tendance des derniers mois

## Limitations

- **Démarrage** : Les stats commencent à s'enregistrer à partir de la première mise à jour après installation
- **Historique** : Pas de récupération automatique des événements passés
- **Noms** : Sensible à la casse (Alice ≠ alice)
- **Doublons** : Un même événement peut être enregistré plusieurs fois si le nom change
- **Volume** : Le fichier stats.json peut devenir volumineux avec le temps

## Évolutions futures possibles

- 📊 Export Excel/CSV des statistiques
- 📈 Graphiques de tendances (avec matplotlib)
- 🔔 Alertes sur baisse de participation
- 🎯 Objectifs de participation
- 🏅 Badges/réalisations pour les participant·e·s
- 📧 Rapports mensuels automatiques
- 🔄 Import/export des statistiques
- 🎲 Statistiques par jeu joué (si tracké)

## Dépannage

### Le fichier stats.json n'est pas créé
→ Vérifier les permissions d'écriture du répertoire
→ Le bot doit avoir accès en écriture à `/app`

### Les statistiques ne se mettent pas à jour
→ Vérifier que la mise à jour des participants fonctionne
→ Consulter les logs : `docker compose logs -f`

### Fichier stats.json corrompu
→ Restaurer depuis la sauvegarde
→ Ou réinitialiser avec structure vide

### Doublons dans les statistiques
→ Normal si un événement est mis à jour plusieurs fois
→ La déduplication se fait automatiquement par (date, nom)

## Support

Pour toute question ou bug concernant les statistiques :
1. Vérifier ce document
2. Consulter les logs du bot
3. Ouvrir une issue sur GitHub
4. Contacter l'administrateur du bot
