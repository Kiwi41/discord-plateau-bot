#!/usr/bin/env python3
"""
Bot Discord pour Soirées Plateaux
Crée automatiquement des posts hebdomadaires pour planifier les soirées jeux de plateau.
"""

import os
import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import asyncio
import locale
from dotenv import load_dotenv
import pytz
from stats_manager import StatsManager

# Charger les variables d'environnement
load_dotenv()

# Configuration
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))
FORUM_CHANNEL_ID = int(os.getenv('FORUM_CHANNEL_ID'))
REGISTRATION_URL = os.getenv('REGISTRATION_URL', 'https://example.com/inscription')
EVENT_ID = os.getenv('EVENT_ID')
EVENT_DESCRIPTION = os.getenv('EVENT_DESCRIPTION', '🎲 Soirée Plateaux du Vendredi ! 🎲').replace('\\n', '\n')
EVENT_LOCATION = os.getenv('EVENT_LOCATION', 'Le Cube en Bois')
TIMEZONE = os.getenv('TIMEZONE', 'Europe/Paris')
DRY_RUN = os.getenv('DRY_RUN', 'false').lower() == 'true'
AUTO_PROCESS = os.getenv('AUTO_PROCESS', 'false').lower() == 'true'

# Configuration du fuseau horaire
tz = pytz.timezone(TIMEZONE)

# Configuration du bot
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Initialiser le gestionnaire de statistiques
stats_manager = StatsManager('stats.json')

# Définir la locale française pour le formatage des dates
try:
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'fr_FR')
    except locale.Error:
        print("⚠️  Impossible de définir la locale française, utilisation de la locale par défaut")


def get_next_friday():
    """Obtenir le prochain vendredi."""
    now = datetime.now(tz)
    day_of_week = now.weekday()  # 0 = lundi, 4 = vendredi, 5 = samedi
    
    if day_of_week == 5:  # Samedi
        days_until_friday = 6
    elif day_of_week == 4 and now.hour >= 18:  # Vendredi après 18h
        days_until_friday = 7
    else:
        days_until_friday = (4 - day_of_week) % 7
        if days_until_friday == 0:
            days_until_friday = 7
    
    next_friday = now + timedelta(days=days_until_friday)
    return next_friday.replace(hour=0, minute=0, second=0, microsecond=0)


def get_next_four_fridays():
    """Obtenir les 4 prochains vendredis."""
    fridays = []
    current_friday = get_next_friday()
    
    for i in range(4):
        fridays.append(current_friday)
        current_friday = current_friday + timedelta(days=7)
    
    return fridays


def format_date(date):
    """Formater la date en français."""
    try:
        # Capitaliser le premier caractère (jour de la semaine)
        formatted = date.strftime('%A %d %B %Y')
        return formatted[0].upper() + formatted[1:]
    except Exception as e:
        print(f"⚠️  Erreur de formatage de date: {e}")
        return date.strftime('%Y-%m-%d')


async def fetch_discord_events_with_retry(guild, max_retries=3):
    """Récupérer les événements Discord avec retry."""
    for attempt in range(1, max_retries + 1):
        try:
            print(f"📡 Tentative {attempt}/{max_retries} de récupération des événements...")
            
            events = await asyncio.wait_for(
                guild.fetch_scheduled_events(),
                timeout=15.0
            )
            
            print(f"✅ {len(events)} événements trouvés sur le serveur")
            return events
            
        except asyncio.TimeoutError:
            print(f"⚠️  Tentative {attempt}/{max_retries} échouée: Timeout")
        except Exception as error:
            print(f"⚠️  Tentative {attempt}/{max_retries} échouée: {error}")
        
        if attempt < max_retries:
            wait_time = attempt * 2
            print(f"⏳ Pause de {wait_time} secondes avant nouvelle tentative...")
            await asyncio.sleep(wait_time)
    
    return None


def find_friday_event(all_events, target_date):
    """Trouver l'événement Discord du vendredi."""
    try:
        print(f"🔍 Recherche d'événements pour {target_date.date()}...")
        
        if not all_events:
            print("⚠️  Aucun événement disponible, utilisation des valeurs par défaut")
            return None
        
        print(f"📅 Recherche dans {len(all_events)} événements")
        
        # Chercher un événement qui correspond à la date du vendredi
        for event in all_events:
            if not event.start_time:
                continue
            
            event_date = event.start_time.date()
            target_day = target_date.date()
            
            # Recherche plus flexible : plateau, soirée, jeu, etc.
            event_name = event.name.lower()
            keywords = ['plateau', 'soirée', 'jeu', 'board', 'game']
            has_keyword = any(keyword in event_name for keyword in keywords)
            
            # Log des événements examinés
            print(f"   🔎 Examen: '{event.name}' - Date: {event_date} - Cible: {target_day} - Match: {event_date == target_day and has_keyword}")
            
            if event_date == target_day and has_keyword:
                print(f"✅ Événement correspondant trouvé: {event.name}")
                return event
        
        print(f"❌ Aucun événement trouvé pour {target_date.date()}")
        return None
        
    except Exception as error:
        print(f"⚠️  Erreur lors de la recherche d'événements: {error}")
        return None


async def create_discord_event(guild, friday_date):
    """Créer un événement Discord pour un vendredi."""
    try:
        # Préparer la date et l'heure de l'événement (20h30)
        event_start = friday_date.replace(hour=20, minute=30, second=0, microsecond=0)
        event_end = event_start + timedelta(hours=4)  # Jusqu'à 00h30
        
        # Nom de l'événement
        event_name = f"Soirée Plateaux - {format_date(friday_date)}"
        
        # Parser le lieu
        location = EVENT_LOCATION
        
        print(f"🎯 Création de l'événement Discord: {event_name}")
        print(f"   📅 Date: {event_start.strftime('%d/%m/%Y %H:%M')}")
        print(f"   📍 Lieu: {location}")
        
        if DRY_RUN:
            print(f"🧪 [DRY RUN] Événement qui serait créé:")
            print(f"   Nom: {event_name}")
            print(f"   Description: {EVENT_DESCRIPTION[:100]}...")
            print(f"   Lieu: {location}")
            return None
        
        # Créer l'événement Discord
        event = await guild.create_scheduled_event(
            name=event_name,
            description=EVENT_DESCRIPTION,
            start_time=event_start,
            end_time=event_end,
            location=location,
            entity_type=discord.EntityType.external,
            privacy_level=discord.PrivacyLevel.guild_only
        )
        
        print(f"✅ Événement Discord créé: {event.name} (ID: {event.id})")
        return event
        
    except Exception as error:
        print(f"❌ Erreur lors de la création de l'événement Discord: {error}")
        return None


async def get_event_participants(event, recurring_event=None):
    """Récupérer la liste des personnes inscrites à un événement Discord."""
    try:
        # Récupérer les utilisateurs intéressés par l'événement
        personnes_inscrites = {}  # Utiliser un dict pour éviter les doublons (clé = user.id)
        
        print(f"🔍 Récupération des participant·e·s pour l'événement: {event.name} (ID: {event.id})")
        
        # Récupérer les participant·e·s de l'événement principal
        async for user in event.users():
            if not user.bot:  # Ignorer les bots
                personnes_inscrites[user.id] = user
                print(f"   👤 Participant·e trouvé·e sur l'événement principal: {user.display_name}")
        
        # Si un événement récurrent est fourni, récupérer aussi ses participant·e·s
        if recurring_event and recurring_event.id != event.id:
            print(f"🔍 Récupération des participant·e·s de l'événement récurrent: {recurring_event.name} (ID: {recurring_event.id})")
            async for user in recurring_event.users():
                if not user.bot:
                    if user.id not in personnes_inscrites:
                        personnes_inscrites[user.id] = user
                        print(f"   👤 Participant·e trouvé·e sur l'événement récurrent: {user.display_name}")
                    else:
                        print(f"   ✓ {user.display_name} déjà compté·e (inscrit·e sur les deux)")
        
        participants_list = list(personnes_inscrites.values())
        print(f"✅ Total: {len(participants_list)} personne·s inscrite·s (après déduplication)")
        return participants_list
        
    except Exception as error:
        print(f"⚠️  Erreur lors de la récupération des participant·e·s: {error}")
        return []


async def update_post_participants(post, event, recurring_event=None):
    """Mettre à jour la liste des personnes inscrites dans un post existant."""
    try:
        # Récupérer les personnes inscrites à l'événement (et à l'événement récurrent si fourni)
        personnes_inscrites = await get_event_participants(event, recurring_event)
        
        # Récupérer le premier message du post (le message principal)
        first_message = await anext(post.history(limit=1, oldest_first=True))
        
        if not first_message or not first_message.embeds:
            return False
        
        # Copier l'embed existant
        old_embed = first_message.embeds[0]
        new_embed = discord.Embed(
            title=old_embed.title,
            description=old_embed.description,
            color=old_embed.color,
            timestamp=old_embed.timestamp
        )
        
        # Copier tous les champs existants sauf celui des personnes inscrites
        for field in old_embed.fields:
            if not field.name.startswith('👥'):
                new_embed.add_field(name=field.name, value=field.value, inline=field.inline)
        
        # Ajouter ou mettre à jour le champ des personnes inscrites
        if personnes_inscrites:
            count = len(personnes_inscrites)
            names = ', '.join([p.display_name for p in personnes_inscrites[:10]])  # Limiter à 10 noms
            
            if count > 10:
                names += f'... et {count - 10} autre(s)'
            
            inscriptions_text = f"**{count} personne(s) inscrite(s)**\n{names}"
        else:
            inscriptions_text = "Aucune inscription pour le moment"
        
        new_embed.add_field(name='👥 Inscriptions', value=inscriptions_text, inline=False)
        
        # Copier le footer
        if old_embed.footer:
            new_embed.set_footer(text=old_embed.footer.text)
        
        # Vérifier si le contenu a changé
        old_inscriptions_field = None
        for field in old_embed.fields:
            if field.name.startswith('👥'):
                old_inscriptions_field = field.value
                break
        
        new_inscriptions_field = inscriptions_text
        
        if old_inscriptions_field == new_inscriptions_field:
            return False  # Pas de changement
        
        # Mettre à jour le message
        if DRY_RUN:
            print("\n🧪 [DRY RUN] Inscriptions qui seraient mises à jour:")
            print(f"   👥 {inscriptions_text}")
            print()
        else:
            await first_message.edit(embed=new_embed)
        print(f"✅ Liste des inscriptions mise à jour: {len(personnes_inscrites)} personne(s)")
        return True
        
    except Exception as error:
        print(f"❌ Erreur lors de la mise à jour des inscriptions: {error}")
        return False


async def check_for_duplicates(forum_channel, post_title):
    """Vérifier les doublons dans le forum."""
    try:
        all_threads = []
        
        # Récupérer les threads actifs (non archivés)
        # Pour un ForumChannel, on doit utiliser fetch sur les threads actifs
        try:
            # Les threads actifs sont accessibles via l'attribut threads du forum
            # Mais il faut d'abord les charger depuis l'API
            active_threads = forum_channel.threads
            for thread in active_threads:
                all_threads.append(thread)
                print(f"   📌 Thread actif trouvé: {thread.name}")
        except Exception as e:
            print(f"⚠️  Erreur lors de la récupération des threads actifs: {e}")
        
        # Récupérer les threads archivés publics
        try:
            async for thread in forum_channel.archived_threads(limit=100):
                all_threads.append(thread)
                print(f"   📦 Thread archivé trouvé: {thread.name}")
        except Exception as e:
            print(f"⚠️  Erreur lors de la récupération des threads archivés: {e}")
        
        print(f"🔍 Total de {len(all_threads)} threads trouvés dans le forum")
        
        # Chercher un thread avec le même titre (insensible à la casse)
        # Privilégier les threads actifs (non archivés)
        matching_thread = None
        post_title_lower = post_title.lower()
        
        for thread in all_threads:
            if thread.name.lower() == post_title_lower:
                if not thread.archived:
                    # Thread actif trouvé, on le retourne immédiatement
                    print(f"✅ Post actif trouvé: {thread.name} (ID: {thread.id})")
                    return thread
                elif not matching_thread:
                    # Garder le premier thread archivé trouvé comme backup
                    matching_thread = thread
        
        if matching_thread:
            print(f"⚠️  Post existant trouvé: {matching_thread.name} (ID: {matching_thread.id})")
            
        return matching_thread
        
    except Exception as error:
        print(f"⚠️  Impossible de vérifier les doublons: {error}")
        return None


async def update_existing_post(thread, embed, event_info):
    """Mettre à jour un post existant."""
    try:
        # Récupérer le premier message du thread
        async for message in thread.history(limit=10, oldest_first=True):
            if message.author == bot.user:
                # Vérifier si le contenu a changé
                if not message.embeds:
                    print("🔄 Aucun embed trouvé, mise à jour du message")
                    await message.edit(embed=embed)
                    return True
                
                current_embed = message.embeds[0]
                current_fields = {field.name: field.value for field in current_embed.fields}
                
                # Extraction des anciennes valeurs
                old_time = current_fields.get('🕖 Heure', '')
                old_location = current_fields.get('📍 Lieu', '')
                old_event_text = current_fields.get('🎯 Événement Discord', '')
                old_inscriptions = current_fields.get('👥 Inscriptions', '')
                old_description = current_embed.description or ''
                
                # Extraction des nouvelles valeurs depuis le nouvel embed
                new_fields = {field.name: field.value for field in embed.fields}
                new_time = new_fields.get('🕖 Heure', '')
                new_location = new_fields.get('📍 Lieu', '')
                new_event_text = new_fields.get('🎯 Événement Discord', '')
                new_inscriptions = new_fields.get('👥 Inscriptions', '')
                new_description = embed.description or ''
                
                # Logs de debugging
                print("🔍 Comparaison des valeurs:")
                print(f"   🕖 Heure: '{old_time}' vs '{new_time}' → {'identique' if old_time == new_time else 'différent'}")
                print(f"   📍 Lieu: '{old_location}' vs '{new_location}' → {'identique' if old_location == new_location else 'différent'}")
                print(f"   🎯 Événement: '{old_event_text}' vs '{new_event_text}' → {'identique' if old_event_text == new_event_text else 'différent'}")
                print(f"   👥 Inscriptions: {len(old_inscriptions)} vs {len(new_inscriptions)} caractères → {'identique' if old_inscriptions == new_inscriptions else 'différent'}")
                print(f"   📝 Description: {len(old_description)} vs {len(new_description)} caractères → {'identique' if old_description == new_description else 'différent'}")
                
                # Comparaison avec les nouvelles valeurs
                has_time_changed = old_time != new_time
                has_location_changed = old_location != new_location
                has_event_text_changed = old_event_text != new_event_text
                has_inscriptions_changed = old_inscriptions != new_inscriptions
                has_description_changed = old_description != new_description
                
                if any([has_time_changed, has_location_changed, has_event_text_changed, has_inscriptions_changed, has_description_changed]):
                    print("🔄 Mise à jour détectée:")
                    if has_time_changed:
                        print(f"   🕖 Heure: '{old_time}' → '{new_time}'")
                    if has_location_changed:
                        print(f"   📍 Lieu: '{old_location}' → '{new_location}'")
                    if has_event_text_changed:
                        print(f"   🎯 Événement: '{old_event_text}' → '{new_event_text}'")
                    if has_inscriptions_changed:
                        print(f"   👥 Inscriptions: changées ({len(old_inscriptions)} → {len(new_inscriptions)} caractères)")
                    if has_description_changed:
                        print(f"   📝 Description: changée ({len(old_description)} → {len(new_description)} caractères)")
                    
                    if DRY_RUN:
                        print("\n🧪 [DRY RUN] Message qui serait édité:")
                        print(f"   📝 Titre: {embed.title}")
                        print(f"   📋 Description: {embed.description[:100]}...")
                        for field in embed.fields:
                            print(f"   • {field.name}: {field.value[:50]}...")
                        print()
                    else:
                        await message.edit(embed=embed)
                    return True
                else:
                    print("✅ Aucune mise à jour nécessaire")
                    return False
                
                # Enregistrer les stats si la mise à jour a eu lieu
                if participant_list:
                    try:
                        event_date_iso = friday_date.isoformat()
                        event_name = f"Soirée Plateaux - {format_date(friday_date)}"
                        participant_names = [p.strip() for p in participant_list]
                        stats_manager.record_event(
                            event_date=event_date_iso,
                            event_name=event_name,
                            participants=participant_names,
                            event_id=str(event.id) if event else None
                        )
                    except Exception as stats_error:
                        print(f"⚠️ Erreur lors de l'enregistrement des stats: {stats_error}")
                
                break
        
        return False
        
    except Exception as error:
        print(f"❌ Erreur lors de la mise à jour du post: {error}")
        return False


async def process_one_friday(guild, forum_channel, friday_date, all_events=None):
    """Traiter un vendredi spécifique (création ou mise à jour)."""
    formatted_date = format_date(friday_date)
    post_title = f"Soirée Plateaux - {formatted_date}"
    
    print(f"📅 Traitement du {formatted_date}...")
    
    # Vérification des doublons
    existing_post = await check_for_duplicates(forum_channel, post_title)
    
    # Recherche de l'événement spécifique du vendredi
    print(f"🔍 Recherche d'un événement spécifique pour {formatted_date}...")
    friday_event = find_friday_event(all_events, friday_date)
    print(f"📋 Événement trouvé: {friday_event.name if friday_event else 'Aucun'}")
    
    # Si aucun événement n'existe, en créer un automatiquement
    if not friday_event:
        print(f"🎯 Aucun événement trouvé, création automatique...")
        friday_event = await create_discord_event(guild, friday_date)
        if friday_event:
            print(f"✅ Événement créé automatiquement: {friday_event.name}")
    
    # Variables pour les informations de l'événement
    event_time = '20:30'
    event_location = '📍 [Le Cube en Bois](https://www.google.com/maps/place/Le+D%C3%A9mon+du+Jeu/@47.6239545,1.3247093,214m)'
    event_url = REGISTRATION_URL
    event_text = f'[Lien d\'inscription]({event_url})'
    recurring_event_data = None
    
    if friday_event:
        # Récupération des informations depuis l'événement Discord
        event_start = friday_event.start_time.astimezone(tz)
        event_time = event_start.strftime('%H:%M')
        
        # Récupération du lieu selon le type d'événement
        if friday_event.entity_type == discord.EntityType.external:
            if friday_event.location:
                location = friday_event.location
                # Nettoyer le lieu si c'est un lien Google Maps
                if 'https://www.google.com/maps' in location:
                    parts = location.split(' – ')
                    if len(parts) > 1:
                        place_name = parts[0].strip()
                        map_url = parts[1].strip()
                        event_location = f"📍 [{place_name}]({map_url})"
                    else:
                        event_location = f"📍 {location}"
                else:
                    event_location = f"📍 {location}"
            else:
                event_location = 'Lieu externe (non spécifié)'
        elif friday_event.entity_type == discord.EntityType.voice:
            if friday_event.channel:
                event_location = f"🔊 {friday_event.channel.name}"
            else:
                event_location = 'Canal vocal (non spécifié)'
        elif friday_event.entity_type == discord.EntityType.stage_instance:
            if friday_event.channel:
                event_location = f"🎪 Scène: {friday_event.channel.name}"
            else:
                event_location = 'Scène (non spécifiée)'
        
        event_url = f"https://discord.com/events/{GUILD_ID}/{friday_event.id}"
        event_text = f"[Rejoindre l'événement]({event_url})"
        print(f"✅ Événement spécifique trouvé: {friday_event.name}")
        print(f"🕖 Heure de l'événement: {event_time}")
        print(f"📍 Lieu de l'événement: {event_location}")
        
    elif EVENT_ID:
        # Chercher l'événement récurrent dans la liste déjà récupérée
        try:
            print(f"🔍 Recherche de l'événement récurrent ID: {EVENT_ID} dans la liste")
            
            recurring_event = None
            if all_events:
                for event in all_events:
                    if str(event.id) == str(EVENT_ID):
                        recurring_event = event
                        break
            
            if not recurring_event:
                print(f"⚠️ Événement récurrent non trouvé dans la liste, tentative de récupération directe...")
                recurring_event = await asyncio.wait_for(
                    guild.fetch_scheduled_event(int(EVENT_ID)),
                    timeout=5.0
                )
            
            if recurring_event:
                print(f"✅ Événement récurrent trouvé: {recurring_event.name}")
                if recurring_event.description:
                    print(f"📝 Description de l'événement récurrent: {len(recurring_event.description)} caractères")
                else:
                    print(f"⚠️ Pas de description sur l'événement récurrent")
            
            if recurring_event and recurring_event.start_time:
                event_start = recurring_event.start_time.astimezone(tz)
                event_time = event_start.strftime('%H:%M')
                
                # Récupération du lieu
                if recurring_event.entity_type == discord.EntityType.external:
                    if recurring_event.location:
                        location = recurring_event.location
                        if 'https://www.google.com/maps' in location:
                            parts = location.split(' – ')
                            if len(parts) > 1:
                                place_name = parts[0].strip()
                                map_url = parts[1].strip()
                                event_location = f"📍 [{place_name}]({map_url})"
                            else:
                                event_location = f"📍 {location}"
                        else:
                            event_location = f"📍 {location}"
                
                event_url = f"https://discord.com/events/{GUILD_ID}/{EVENT_ID}"
                event_text = f"[Rejoindre l'événement Discord]({event_url})"
                recurring_event_data = recurring_event
                print("✅ Événement récurrent récupéré avec succès")
            
        except Exception as error:
            print(f"❌ Impossible de récupérer l'événement récurrent: {error}")
    
    # Description de l'embed
    embed_description = 'Rejoignez-nous pour une soirée jeux de plateau conviviale !'
    
    if friday_event and friday_event.description:
        embed_description = friday_event.description
        print(f"📝 Utilisation de la description de l'événement spécifique: {len(friday_event.description)} caractères")
    elif friday_event and not friday_event.description:
        print("⚠️  Événement trouvé mais sans description, utilisation de la description par défaut")
        embed_description = f"""🎲 **Soirée Plateaux du vendredi !**

Venez découvrir et jouer à une grande variété de jeux de plateau dans une ambiance conviviale !

🎯 **Au programme :**
• Jeux de stratégie, coopératifs, party games...
• Accueil des débutants et confirmés
• Ambiance détendue et bonne humeur garantie

**Rendez-vous {event_time} pour une soirée inoubliable !** 🎉"""
        print("📝 Utilisation de la description par défaut (événement sans description)")
    elif recurring_event_data and recurring_event_data.description:
        embed_description = recurring_event_data.description
        print("📝 Utilisation de la description de l'événement récurrent")
    else:
        embed_description = f"""🎲 **Soirée Plateaux du vendredi !**

Venez découvrir et jouer à une grande variété de jeux de plateau dans une ambiance conviviale !

🎯 **Au programme :**
• Jeux de stratégie, coopératifs, party games...
• Accueil des débutants et confirmés
• Ambiance détendue et bonne humeur garantie

**Rendez-vous {event_time} pour une soirée inoubliable !** 🎉"""
        print("📝 Utilisation de la description par défaut (aucun événement trouvé)")
    
    # Création de l'embed pour le message
    embed = discord.Embed(
        title='🎲 Soirée Plateaux du Vendredi ! 🎲',
        description=embed_description,
        color=0x7289DA,
        timestamp=datetime.now(tz)
    )
    
    embed.add_field(name='📅 Date', value=formatted_date, inline=True)
    embed.add_field(name='🕖 Heure', value=event_time, inline=True)
    embed.add_field(name='📍 Lieu', value=event_location, inline=True)
    embed.add_field(name='🎯 Événement Discord', value=event_text, inline=False)
    
    # Ajouter le champ des inscriptions si un événement est trouvé (spécifique ou récurrent)
    event_for_participants = friday_event or recurring_event_data
    if event_for_participants:
        personnes_inscrites = await get_event_participants(event_for_participants)
        if personnes_inscrites:
            count = len(personnes_inscrites)
            names = ', '.join([p.display_name for p in personnes_inscrites[:10]])
            if count > 10:
                names += f'... et {count - 10} autre(s)'
            inscriptions_text = f"**{count} personne(s) inscrite(s)**\n{names}"
        else:
            inscriptions_text = "Aucune inscription pour le moment"
        embed.add_field(name='👥 Inscriptions', value=inscriptions_text, inline=False)
    
    embed.set_footer(text='Bot Soirées Plateaux')
    
    # Informations pour la comparaison de mise à jour
    event_info = {
        'date': formatted_date,
        'time': event_time,
        'location': event_location,
        'event_text': event_text,
        'description': embed_description
    }
    
    if existing_post:
        # Vérifier si le post est archivé
        if existing_post.archived:
            print(f"⚠️  Post archivé (impossible de mettre à jour): {post_title}")
            return {'action': 'error', 'error': 'Thread is archived', 'thread': existing_post}
        
        # Post existant - vérifier s'il faut le mettre à jour
        was_updated = await update_existing_post(existing_post, embed, event_info)
        if was_updated:
            print(f"🔄 Post mis à jour: {post_title}")
            return {'action': 'updated', 'thread': existing_post}
        else:
            print(f"✅ Post déjà à jour: {post_title}")
            return {'action': 'unchanged', 'thread': existing_post}
    else:
        # Créer un nouveau post
        try:
            if DRY_RUN:
                print("\n🧪 [DRY RUN] Post qui serait créé:")
                print(f"   📌 Titre: {post_title}")
                print(f"   📝 Titre embed: {embed.title}")
                print(f"   📋 Description: {embed.description}")
                print("   📊 Champs:")
                for field in embed.fields:
                    print(f"      • {field.name}: {field.value}")
                print(f"   🎨 Couleur: {hex(embed.color.value)}")
                print(f"   ⏰ Timestamp: {embed.timestamp}")
                print()
                return {'action': 'created', 'thread': None}
            else:
                thread = await forum_channel.create_thread(
                    name=post_title,
                    embed=embed
                )
                
                print(f"✅ Nouveau post créé: {post_title}")
                print(f"🔗 Lien: https://discord.com/channels/{GUILD_ID}/{thread.thread.id}")
                return {'action': 'created', 'thread': thread.thread}
            
        except Exception as error:
            print(f"❌ Erreur lors de la création du post pour {formatted_date}: {error}")
            return {'action': 'error', 'error': error}


async def process_next_four_fridays():
    """Créer/mettre à jour les 4 prochains vendredis."""
    try:
        print("🔄 Traitement des 4 prochains vendredis...")
        
        guild = bot.get_guild(GUILD_ID)
        if not guild:
            print("❌ Serveur Discord non trouvé")
            return
        
        forum_channel = guild.get_channel(FORUM_CHANNEL_ID)
        if not forum_channel:
            print("❌ Canal forum non trouvé")
            return
        
        # Obtenir les 4 prochains vendredis
        fridays = get_next_four_fridays()
        print("📅 Les 4 prochains vendredis à traiter:")
        for i, friday in enumerate(fridays, 1):
            print(f"   {i}. {format_date(friday)}")
        
        # Récupérer tous les événements avec retry
        print("🔍 Récupération des événements Discord...")
        all_events = None
        
        try:
            all_events = await fetch_discord_events_with_retry(guild)
            if not all_events:
                print("⚠️  Impossible de récupérer les événements Discord après plusieurs tentatives")
                print("🔄 Le traitement continuera avec les valeurs par défaut")
        except Exception as error:
            print(f"❌ Erreur fatale lors de la récupération des événements: {error}")
        
        results = {
            'created': 0,
            'updated': 0,
            'unchanged': 0,
            'errors': 0
        }
        
        # Traiter chaque vendredi
        for i, friday in enumerate(fridays):
            print(f"\n🔄 Traitement {i + 1}/4: {format_date(friday)}")
            
            try:
                print(f"🚀 Début du traitement pour {format_date(friday)}...")
                result = await process_one_friday(guild, forum_channel, friday, all_events)
                print(f"✅ Fin du traitement pour {format_date(friday)}")
                
                print(f"📊 Résultat pour {format_date(friday)}: {result['action']}")
                
                action = result['action']
                if action == 'created':
                    results['created'] += 1
                elif action == 'updated':
                    results['updated'] += 1
                elif action == 'unchanged':
                    results['unchanged'] += 1
                elif action == 'error':
                    results['errors'] += 1
                    print(f"❌ Erreur pour {format_date(friday)}: {result.get('error')}")
                
                # Petite pause entre chaque traitement
                if i < len(fridays) - 1:
                    print("⏳ Pause de 2 secondes avant le vendredi suivant...")
                    await asyncio.sleep(2)
                    print("✅ Fin de pause, continuons avec le vendredi suivant...")
                
            except Exception as error:
                print(f"❌ Erreur lors du traitement de {format_date(friday)}: {error}")
                results['errors'] += 1
                
                if i < len(fridays) - 1:
                    print("⏳ Pause de 2 secondes après l'erreur...")
                    await asyncio.sleep(2)
        
        # Résumé final
        print("\n📋 Résumé du traitement:")
        print(f"   ✅ {results['created']} posts créés")
        print(f"   🔄 {results['updated']} posts mis à jour")
        print(f"   ⚪ {results['unchanged']} posts inchangés")
        print(f"   ❌ {results['errors']} erreurs")
        
    except Exception as error:
        print(f"❌ Erreur lors du traitement des posts: {error}")


async def create_forum_post():
    """Créer/mettre à jour le post pour le prochain vendredi."""
    try:
        print("🔄 Tentative de création du post pour le prochain vendredi...")
        
        guild = bot.get_guild(GUILD_ID)
        if not guild:
            print("❌ Serveur Discord non trouvé")
            return
        
        forum_channel = guild.get_channel(FORUM_CHANNEL_ID)
        if not forum_channel:
            print("❌ Canal forum non trouvé")
            return
        
        # Récupérer les événements Discord
        print("🔍 Récupération des événements Discord...")
        all_events = None
        
        try:
            all_events = await fetch_discord_events_with_retry(guild)
            if not all_events:
                print("⚠️  Impossible de récupérer les événements Discord après plusieurs tentatives")
                print("🔄 Le traitement continuera avec les valeurs par défaut")
        except Exception as error:
            print(f"❌ Erreur fatale lors de la récupération des événements: {error}")
        
        next_friday = get_next_friday()
        result = await process_one_friday(guild, forum_channel, next_friday, all_events)
        
        if result['action'] == 'error':
            print(f"❌ Erreur lors du traitement: {result.get('error')}")
        
    except Exception as error:
        print(f"❌ Erreur lors de la création du post: {error}")


@bot.event
async def on_ready():
    """Événement quand le bot est prêt."""
    print(f"🤖 Bot connecté en tant que {bot.user.name}#{bot.user.discriminator}!")
    print(f"📊 Serveurs: {len(bot.guilds)}")
    print(f"👥 Utilisateurs: {len(bot.users)}")
    
    if DRY_RUN:
        print("\n🧪 MODE TEST ACTIVÉ (DRY_RUN=true)")
        print("   ⚠️  Aucune modification ne sera effectuée sur Discord")
        print("   📋 Les actions seront affichées dans le terminal\n")
    
    # Afficher les serveurs où le bot est présent
    print("🏠 Serveurs où le bot est présent:")
    for guild in bot.guilds:
        print(f"   - {guild.name} (ID: {guild.id})")
    
    print("🕒 Planification active: Samedis à 3h00 (Europe/Paris)")
    print("📝 Commandes manuelles:")
    print("   - !create-plateau-post (prochain vendredi)")
    print("   - !process-next-month (4 prochains vendredis)")
    print("   - !plateau-help (aide)")
    
    # Démarrer les tâches planifiées
    if not scheduled_task.is_running():
        scheduled_task.start()
    if not update_participants_task.is_running():
        update_participants_task.start()
        print("👥 Mise à jour des inscriptions activée (toutes les 15 minutes)")
    
    # Exécution automatique si AUTO_PROCESS est activé
    if AUTO_PROCESS:
        print("\n🚀 AUTO_PROCESS activé - Lancement du traitement automatique...")
        await process_next_four_fridays()
        print("\n✅ Traitement automatique terminé!")
        if DRY_RUN:
            print("   (Mode test - aucune modification sur Discord)\n")


@tasks.loop(hours=24)
async def scheduled_task():
    """Tâche planifiée pour créer les posts tous les samedis à 3h00."""
    now = datetime.now(tz)
    
    # Vérifier si c'est samedi à 3h00
    if now.weekday() == 5 and now.hour == 3:  # 5 = samedi
        print("⏰ Tâche planifiée déclenchée - Traitement des 4 prochains vendredis (Samedi 3h00)")
        await process_next_four_fridays()


@tasks.loop(minutes=15)
async def update_participants_task():
    """Tâche qui met à jour la liste des inscriptions toutes les 15 minutes."""
    try:
        print("👥 Mise à jour de la liste des inscriptions...")
        
        guild = bot.get_guild(GUILD_ID)
        if not guild:
            print("❌ Serveur Discord non trouvé")
            return
        
        forum_channel = guild.get_channel(FORUM_CHANNEL_ID)
        if not forum_channel:
            print("❌ Canal forum non trouvé")
            return
        
        # Récupérer les événements Discord
        all_events = await fetch_discord_events_with_retry(guild)
        if not all_events:
            print("⚠️  Aucun événement disponible")
            return
        
        # Récupérer les 4 prochains vendredis
        fridays = get_next_four_fridays()
        updated_count = 0
        
        # Récupérer l'événement récurrent une seule fois
        recurring_event = None
        if EVENT_ID:
            for event in all_events:
                if str(event.id) == str(EVENT_ID):
                    recurring_event = event
                    print(f"📅 Événement récurrent trouvé: {event.name} (ID: {EVENT_ID})")
                    break
        
        for friday_date in fridays:
            # Trouver l'événement correspondant (spécifique ou récurrent)
            friday_event = find_friday_event(all_events, friday_date)
            
            # Déterminer quel événement utiliser pour la mise à jour
            event_to_use = friday_event if friday_event else recurring_event
            
            if not event_to_use:
                continue
            
            if not friday_event and recurring_event:
                print(f"📅 Utilisation de l'événement récurrent pour {format_date(friday_date)}")
            elif friday_event and recurring_event:
                print(f"📅 Événement spécifique trouvé, combinaison avec l'événement récurrent pour {format_date(friday_date)}")
            
            # Rechercher le post forum correspondant
            formatted_date = format_date(friday_date)
            post_title = f"Soirée Plateaux - {formatted_date}"
            
            existing_post = await check_for_duplicates(forum_channel, post_title)
            if not existing_post:
                continue
            
            # Vérifier si le post n'est pas archivé
            if existing_post.archived:
                print(f"⏭️  Post archivé ignoré: {post_title}")
                continue
            
            # Mettre à jour les inscriptions
            # Si friday_event existe, on cherche dans friday_event ET recurring_event
            # Sinon on cherche uniquement dans recurring_event
            updated = await update_post_participants(existing_post, event_to_use, recurring_event if friday_event else None)
            if updated:
                updated_count += 1
        
        if updated_count > 0:
            print(f"✅ {updated_count} post(s) mis à jour avec la liste des inscriptions")
        else:
            print("ℹ️  Aucune mise à jour d'inscriptions nécessaire")
            
    except Exception as error:
        print(f"❌ Erreur lors de la mise à jour des inscriptions: {error}")


@bot.event
async def on_message(message):
    """Gestionnaire de messages."""
    # Ignorer les messages des bots
    if message.author.bot:
        return
    
    # Test simple
    if message.content == '!test':
        print("🧪 Test de réponse...")
        await message.reply("✅ Le bot reçoit bien les messages !")
        return
    
    # Traiter les commandes
    await bot.process_commands(message)


@bot.command(name='create-plateau-post')
async def create_plateau_post_command(ctx):
    """Commande pour créer/mettre à jour un post pour le prochain vendredi."""
    await ctx.reply("🔄 Création/mise à jour du post pour le prochain vendredi...")
    await create_forum_post()
    await ctx.send("✅ Traitement terminé!")


@bot.command(name='process-next-month')
async def process_next_month_command(ctx):
    """Commande pour traiter les 4 prochains vendredis."""
    await ctx.reply("📅 Traitement des 4 prochains vendredis en cours...")
    await process_next_four_fridays()
    await ctx.send("✅ Traitement des 4 prochains vendredis terminé!")


@bot.command(name='plateau-next-month')
async def plateau_next_month_command(ctx):
    """Alias pour process-next-month."""
    await process_next_month_command(ctx)


@bot.command(name='process-friday')
async def process_friday_command(ctx, date_str: str):
    """Traite un vendredi spécifique (format: YYYY-MM-DD)."""
    try:
        guild = bot.get_guild(GUILD_ID)
        if not guild:
            await ctx.send("❌ Impossible de trouver le serveur Discord")
            return
        
        forum_channel = guild.get_channel(FORUM_CHANNEL_ID)
        if not forum_channel:
            await ctx.send("❌ Impossible de trouver le canal forum")
            return
        
        friday_date = datetime.strptime(date_str, "%Y-%m-%d")
        friday_date = tz.localize(friday_date)
        
        if friday_date.weekday() != 4:  # 4 = vendredi
            await ctx.send(f"❌ La date {date_str} n'est pas un vendredi!")
            return
        
        await ctx.send(f"🔄 Traitement du vendredi {format_date(friday_date)}...")
        result = await process_one_friday(guild, forum_channel, friday_date)
        
        if result == "created":
            await ctx.send(f"✅ Post créé pour le {format_date(friday_date)}")
        elif result == "updated":
            await ctx.send(f"✅ Post mis à jour pour le {format_date(friday_date)}")
        elif result == "unchanged":
            await ctx.send(f"ℹ️ Aucune modification nécessaire pour le {format_date(friday_date)}")
        else:
            await ctx.send(f"❌ Erreur lors du traitement du {format_date(friday_date)}")
    except ValueError:
        await ctx.send("❌ Format de date invalide. Utilisez YYYY-MM-DD (ex: 2025-12-26)")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")


@bot.command(name='stats')
async def stats_command(ctx, participant_name: str = None):
    """Commande pour afficher les statistiques des soirées plateaux."""
    try:
        if participant_name:
            # Statistiques pour un·e participant·e spécifique
            participant_stats = stats_manager.get_participant_stats(participant_name)
            if not participant_stats:
                await ctx.send(f"❌ Aucune donnée trouvée pour {participant_name}")
                return
            
            embed = discord.Embed(
                title=f'📊 Statistiques de {participant_name}',
                color=0x7289DA,
                timestamp=datetime.now(tz)
            )
            
            embed.add_field(
                name='📈 Participations',
                value=f'**Total:** {participant_stats["total_events"]} soirées',
                inline=False
            )
            
            embed.add_field(
                name='📅 Première participation',
                value=participant_stats['first_attendance'],
                inline=False
            )
            
            # Liste des événements récents
            recent_events = sorted(participant_stats['events_attended'], reverse=True)[:5]
            if recent_events:
                embed.add_field(
                    name='🗓️ Dernières participations',
                    value='\n'.join(recent_events[:5]),
                    inline=False
                )
            
            await ctx.send(embed=embed)
        else:
            # Statistiques générales
            stats = stats_manager.export_stats()
            
            embed = discord.Embed(
                title='📊 Statistiques des Soirées Plateaux',
                description='Vue d\'ensemble de nos soirées jeux',
                color=0x7289DA,
                timestamp=datetime.now(tz)
            )
            
            # Statistiques générales
            embed.add_field(
                name='🎲 Événements',
                value=f'**Total:** {stats["total_events"]} soirées organisées',
                inline=True
            )
            
            embed.add_field(
                name='👥 Participant·e·s uniques',
                value=f'**Total:** {stats["total_unique_participants"]}',
                inline=True
            )
            
            embed.add_field(
                name='📈 Moyenne de participation',
                value=f'**{stats["average_participants"]:.1f}** personnes par soirée',
                inline=True
            )
            
            # Top participants
            if stats['top_participants']:
                top_5 = stats['top_participants'][:5]
                medals = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣']
                top_text = '\n'.join(
                    f'{medals[i]} **{name}** - {count} soirées' 
                    for i, (name, count) in enumerate(top_5)
                )
                embed.add_field(
                    name='🏆 Top 5 des participant·e·s',
                    value=top_text,
                    inline=False
                )
            
            # Tendance récente
            if stats['trend']:
                trend_text = '\n'.join(
                    f'**{t["month"]}**: {t["event_count"]} soirées, {t["avg_participants"]:.1f} personnes en moyenne'
                    for t in stats['trend'][-3:]  # 3 derniers mois
                )
                embed.add_field(
                    name='📊 Tendance récente',
                    value=trend_text,
                    inline=False
                )
            
            # Événements récents
            if stats['recent_events']:
                recent_text = '\n'.join(
                    f'**{e["date"][:10]}** - {e["participant_count"]} participant·e·s'
                    for e in stats['recent_events'][:3]
                )
                embed.add_field(
                    name='📅 Dernières soirées',
                    value=recent_text,
                    inline=False
                )
            
            if stats['first_event_date']:
                embed.set_footer(text=f'Première soirée enregistrée: {stats["first_event_date"][:10]}')
            
            await ctx.send(embed=embed)
    
    except Exception as error:
        print(f"❌ Erreur lors de l'affichage des stats: {error}")
        await ctx.send(f"❌ Erreur: {error}")


@bot.command(name='list-events')
async def list_events_command(ctx):
    """Commande pour lister tous les événements Discord avec leurs IDs."""
    try:
        guild = bot.get_guild(GUILD_ID)
        if not guild:
            await ctx.send("❌ Serveur Discord non trouvé")
            return
        
        # Récupérer tous les événements
        all_events = await fetch_discord_events_with_retry(guild)
        if not all_events:
            await ctx.send("⚠️ Aucun événement disponible")
            return
        
        # Créer l'embed avec la liste des événements
        embed = discord.Embed(
            title='📅 Liste des événements Discord',
            description=f'Total: {len(all_events)} événement(s)',
            color=0x7289DA,
            timestamp=datetime.now(tz)
        )
        
        for event in all_events:
            event_date = event.start_time.strftime('%d/%m/%Y %H:%M') if event.start_time else 'Date non définie'
            has_description = "✅" if event.description else "❌"
            description_length = len(event.description) if event.description else 0
            
            embed.add_field(
                name=f'{event.name}',
                value=f'**ID:** `{event.id}`\n**Date:** {event_date}\n**Description:** {has_description} ({description_length} car.)',
                inline=False
            )
        
        embed.set_footer(text='Copiez l\'ID de l\'événement récurrent dans EVENT_ID')
        await ctx.send(embed=embed)
        
    except Exception as error:
        print(f"❌ Erreur lors de la liste des événements: {error}")
        await ctx.send(f"❌ Erreur: {error}")


@bot.command(name='plateau-help')
async def plateau_help_command(ctx):
    """Commande d'aide."""
    embed = discord.Embed(
        title='🤖 Commandes Bot Soirées Plateaux',
        description='Commandes disponibles:',
        color=0x7289DA,
        timestamp=datetime.now(tz)
    )
    
    embed.add_field(
        name='!create-plateau-post',
        value='Crée ou met à jour le post pour le prochain vendredi',
        inline=False
    )
    embed.add_field(
        name='!process-next-month',
        value='Traite les 4 prochains vendredis (création + mise à jour)',
        inline=False
    )
    embed.add_field(
        name='!plateau-next-month',
        value='Alias pour !process-next-month',
        inline=False
    )
    embed.add_field(
        name='!update-participants',
        value='Force la mise à jour de la liste des inscriptions',
        inline=False
    )
    embed.add_field(
        name='!list-events',
        value='Liste tous les événements Discord avec leurs IDs',
        inline=False
    )
    embed.add_field(
        name='!stats [nom]',
        value='Affiche les statistiques générales ou d\'un·e participant·e',
        inline=False
    )
    embed.add_field(
        name='!plateau-help',
        value='Affiche cette aide',
        inline=False
    )
    
    embed.set_footer(text='🔄 Les inscriptions se mettent à jour automatiquement toutes les 15 minutes')
    
    await ctx.reply(embed=embed)


@bot.command(name='update-participants')
async def update_participants_command(ctx):
    """Commande pour forcer la mise à jour des inscriptions."""
    await ctx.reply("👥 Mise à jour des inscriptions en cours...")
    
    try:
        guild = bot.get_guild(GUILD_ID)
        if not guild:
            await ctx.send("❌ Serveur Discord non trouvé")
            return
        
        forum_channel = guild.get_channel(FORUM_CHANNEL_ID)
        if not forum_channel:
            await ctx.send("❌ Canal forum non trouvé")
            return
        
        # Récupérer les événements Discord
        all_events = await fetch_discord_events_with_retry(guild)
        if not all_events:
            await ctx.send("⚠️ Aucun événement disponible")
            return
        
        # Récupérer les 4 prochains vendredis
        fridays = get_next_four_fridays()
        updated_count = 0
        
        for friday_date in fridays:
            # Trouver l'événement correspondant (spécifique ou récurrent)
            friday_event = find_friday_event(all_events, friday_date)
            
            # Si pas d'événement spécifique, utiliser l'événement récurrent
            if not friday_event and EVENT_ID:
                for event in all_events:
                    if str(event.id) == str(EVENT_ID):
                        friday_event = event
                        print(f"📅 Utilisation de l'événement récurrent pour {format_date(friday_date)}")
                        break
            
            if not friday_event:
                continue
            
            # Rechercher le post forum correspondant
            formatted_date = format_date(friday_date)
            post_title = f"Soirée Plateaux - {formatted_date}"
            
            existing_post = await check_for_duplicates(forum_channel, post_title)
            if not existing_post:
                continue
            
            # Vérifier si le post n'est pas archivé
            if existing_post.archived:
                print(f"⏭️  Post archivé ignoré: {post_title}")
                continue
            
            # Mettre à jour les inscriptions
            updated = await update_post_participants(existing_post, friday_event)
            if updated:
                updated_count += 1
        
        if updated_count > 0:
            await ctx.send(f"✅ {updated_count} post(s) mis à jour avec la liste des inscriptions")
        else:
            await ctx.send("ℹ️ Aucune mise à jour d'inscriptions nécessaire")
            
    except Exception as error:
        print(f"❌ Erreur lors de la mise à jour des inscriptions: {error}")
        await ctx.send(f"❌ Erreur: {error}")


# Lancement du bot
if __name__ == '__main__':
    if not TOKEN:
        print("❌ ERREUR: Token Discord manquant dans les variables d'environnement")
        exit(1)
    
    try:
        bot.run(TOKEN)
    except Exception as error:
        print(f"❌ Erreur lors du démarrage du bot: {error}")
