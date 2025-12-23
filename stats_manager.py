"""
Gestionnaire de statistiques pour le bot Discord Soirées Plateaux
Collecte et analyse les données de participation aux soirées
"""

import json
import os
from datetime import datetime
from collections import Counter
from typing import Dict, List, Optional


class StatsManager:
    """Gère les statistiques des soirées plateaux."""
    
    def __init__(self, stats_file: str = "stats.json"):
        self.stats_file = stats_file
        self.data = self._load_stats()
    
    def _load_stats(self) -> Dict:
        """Charge les statistiques depuis le fichier JSON."""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Erreur lors du chargement des stats: {e}")
                return self._init_empty_stats()
        return self._init_empty_stats()
    
    def _init_empty_stats(self) -> Dict:
        """Initialise une structure de stats vide."""
        return {
            "events": [],
            "participants": {},
            "metadata": {
                "first_event": None,
                "last_updated": None
            }
        }
    
    def _save_stats(self):
        """Sauvegarde les statistiques dans le fichier JSON."""
        try:
            self.data["metadata"]["last_updated"] = datetime.now().isoformat()
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde des stats: {e}")
    
    def record_event(self, event_date: str, event_name: str, participants: List[str], event_id: Optional[str] = None):
        """
        Enregistre un événement et ses participant·e·s.
        
        Args:
            event_date: Date de l'événement (format ISO)
            event_name: Nom de l'événement
            participants: Liste des noms des participant·e·s
            event_id: ID Discord de l'événement (optionnel)
        """
        # Vérifier si l'événement existe déjà
        event_exists = any(
            e.get('date') == event_date and e.get('name') == event_name 
            for e in self.data['events']
        )
        
        if event_exists:
            # Mettre à jour l'événement existant
            for event in self.data['events']:
                if event.get('date') == event_date and event.get('name') == event_name:
                    event['participants'] = participants
                    event['participant_count'] = len(participants)
                    event['updated_at'] = datetime.now().isoformat()
                    if event_id:
                        event['event_id'] = event_id
                    break
        else:
            # Créer un nouvel événement
            event_data = {
                "date": event_date,
                "name": event_name,
                "participants": participants,
                "participant_count": len(participants),
                "event_id": event_id,
                "created_at": datetime.now().isoformat()
            }
            self.data['events'].append(event_data)
            
            # Mettre à jour la date du premier événement
            if not self.data['metadata']['first_event']:
                self.data['metadata']['first_event'] = event_date
        
        # Mettre à jour les statistiques des participant·e·s
        for participant in participants:
            if participant not in self.data['participants']:
                self.data['participants'][participant] = {
                    "total_events": 0,
                    "events_attended": [],
                    "first_attendance": event_date
                }
            
            self.data['participants'][participant]['total_events'] += 1
            if event_date not in self.data['participants'][participant]['events_attended']:
                self.data['participants'][participant]['events_attended'].append(event_date)
        
        self._save_stats()
        print(f"📊 Stats enregistrées: {event_name} - {len(participants)} participant·e·s")
    
    def get_total_events(self) -> int:
        """Retourne le nombre total d'événements enregistrés."""
        return len(self.data['events'])
    
    def get_average_participants(self) -> float:
        """Retourne le nombre moyen de participant·e·s par événement."""
        if not self.data['events']:
            return 0.0
        total = sum(event['participant_count'] for event in self.data['events'])
        return total / len(self.data['events'])
    
    def get_top_participants(self, limit: int = 10) -> List[tuple]:
        """
        Retourne les participant·e·s les plus régulier·e·s.
        
        Returns:
            Liste de tuples (nom, nombre_events)
        """
        participants_counts = [
            (name, data['total_events']) 
            for name, data in self.data['participants'].items()
        ]
        return sorted(participants_counts, key=lambda x: x[1], reverse=True)[:limit]
    
    def get_recent_events(self, limit: int = 5) -> List[Dict]:
        """Retourne les événements les plus récents."""
        sorted_events = sorted(
            self.data['events'], 
            key=lambda x: x['date'], 
            reverse=True
        )
        return sorted_events[:limit]
    
    def get_participant_stats(self, participant_name: str) -> Optional[Dict]:
        """Retourne les statistiques d'un·e participant·e spécifique."""
        return self.data['participants'].get(participant_name)
    
    def get_total_unique_participants(self) -> int:
        """Retourne le nombre total de participant·e·s uniques."""
        return len(self.data['participants'])
    
    def get_participation_trend(self, months: int = 6) -> List[Dict]:
        """
        Retourne la tendance de participation sur les derniers mois.
        
        Returns:
            Liste de dict avec {month: str, count: int, avg_participants: float}
        """
        from datetime import datetime, timedelta
        
        # Calculer la date limite
        now = datetime.now()
        limit_date = now - timedelta(days=months * 30)
        
        # Grouper les événements par mois
        monthly_data = {}
        for event in self.data['events']:
            event_date = datetime.fromisoformat(event['date'])
            if event_date >= limit_date:
                month_key = event_date.strftime('%Y-%m')
                if month_key not in monthly_data:
                    monthly_data[month_key] = {
                        'count': 0,
                        'total_participants': 0
                    }
                monthly_data[month_key]['count'] += 1
                monthly_data[month_key]['total_participants'] += event['participant_count']
        
        # Calculer les moyennes
        result = []
        for month, data in sorted(monthly_data.items()):
            result.append({
                'month': month,
                'event_count': data['count'],
                'avg_participants': data['total_participants'] / data['count'] if data['count'] > 0 else 0
            })
        
        return result
    
    def export_stats(self) -> Dict:
        """Export complet des statistiques pour affichage."""
        return {
            'total_events': self.get_total_events(),
            'total_unique_participants': self.get_total_unique_participants(),
            'average_participants': self.get_average_participants(),
            'top_participants': self.get_top_participants(10),
            'recent_events': self.get_recent_events(5),
            'trend': self.get_participation_trend(6),
            'first_event_date': self.data['metadata'].get('first_event'),
            'last_updated': self.data['metadata'].get('last_updated')
        }
