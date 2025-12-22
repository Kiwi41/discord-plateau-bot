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

# Charger les variables d'environnement
load_dotenv()

# Configuration
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))
FORUM_CHANNEL_ID = int(os.getenv('FORUM_CHANNEL_ID'))
REGISTRATION_URL = os.getenv('REGISTRATION_URL', 'https://example.com/inscription')
EVENT_ID = os.getenv('EVENT_ID')
TIMEZONE = os.getenv('TIMEZONE', 'Europe/Paris')

# Configuration du fuseau horaire
tz = pytz.timezone(TIMEZONE)

# Configuration du bot
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

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
            
            if event_date == target_day and has_keyword:
                return event
        
        return None
        
    except Exception as error:
        print(f"⚠️  Erreur lors de la recherche d'événements: {error}")
        return None


async def get_event_participants(event):
    """Récupérer la liste des personnes inscrites à un événement Discord."""
    try:
        # Récupérer les utilisateurs intéressés par l'événement
        personnes_inscrites = []
        
        # Discord API retourne les utilisateurs intéressés via event.users
        async for user in event.users():
            if not user.bot:  # Ignorer les bots
                personnes_inscrites.append(user)
        
        return personnes_inscrites
        
    except Exception as error:
        print(f"⚠️  Erreur lors de la récupération des participants: {error}")
        return []


async def update_post_participants(post, event):
    """Mettre à jour la liste des personnes inscrites dans un post existant."""
    try:
        # Récupérer les personnes inscrites à l'événement
        personnes_inscrites = await get_event_participants(event)
        
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
        
        # Chercher un thread avec le même titre
        for thread in all_threads:
            if thread.name == post_title:
                print(f"⚠️  Post existant trouvé: {thread.name} (ID: {thread.id})")
                return thread
        
        return None
        
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
                old_description = current_embed.description or ''
                
                # Logs de debugging
                print("🔍 Comparaison des valeurs:")
                print(f"   🕖 Heure: '{old_time}' vs '{event_info['time']}' → {'identique' if old_time == event_info['time'] else 'différent'}")
                print(f"   📍 Lieu: '{old_location}' vs '{event_info['location']}' → {'identique' if old_location == event_info['location'] else 'différent'}")
                print(f"   🎯 Événement: '{old_event_text}' vs '{event_info['event_text']}' → {'identique' if old_event_text == event_info['event_text'] else 'différent'}")
                print(f"   📝 Description: {len(old_description)} vs {len(event_info['description'])} caractères → {'identique' if old_description == event_info['description'] else 'différent'}")
                
                # Comparaison avec les nouvelles valeurs
                has_time_changed = old_time != event_info['time']
                has_location_changed = old_location != event_info['location']
                has_event_text_changed = old_event_text != event_info['event_text']
                has_description_changed = old_description != event_info['description']
                
                if any([has_time_changed, has_location_changed, has_event_text_changed, has_description_changed]):
                    print("🔄 Mise à jour détectée:")
                    if has_time_changed:
                        print(f"   🕖 Heure: '{old_time}' → '{event_info['time']}'")
                    if has_location_changed:
                        print(f"   📍 Lieu: '{old_location}' → '{event_info['location']}'")
                    if has_event_text_changed:
                        print(f"   🎯 Événement: '{old_event_text}' → '{event_info['event_text']}'")
                    if has_description_changed:
                        print(f"   📝 Description: changée ({len(old_description)} → {len(event_info['description'])} caractères)")
                    
                    await message.edit(embed=embed)
                    return True
                else:
                    print("✅ Aucune mise à jour nécessaire")
                    return False
                
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
        # Essayer de récupérer l'événement récurrent
        try:
            print(f"🔍 Tentative de récupération de l'événement récurrent ID: {EVENT_ID}")
            
            recurring_event = await asyncio.wait_for(
                guild.fetch_scheduled_event(int(EVENT_ID)),
                timeout=5.0
            )
            
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
        print("📝 Utilisation de la description de l'événement spécifique")
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
        print("📝 Utilisation de la description par défaut")
    
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
        
        for friday_date in fridays:
            # Trouver l'événement correspondant
            friday_event = find_friday_event(all_events, friday_date)
            if not friday_event:
                continue
            
            # Rechercher le post forum correspondant
            formatted_date = friday_date.strftime('%A %d %B %Y').capitalize()
            post_title = f"Soirée Plateaux - {formatted_date}"
            
            existing_post = await check_for_duplicates(forum_channel, post_title)
            if not existing_post:
                continue
            
            # Mettre à jour les inscriptions
            updated = await update_post_participants(existing_post, friday_event)
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
    await update_participants_task()
    await ctx.send("✅ Mise à jour des inscriptions terminée!")


# Lancement du bot
if __name__ == '__main__':
    if not TOKEN:
        print("❌ ERREUR: Token Discord manquant dans les variables d'environnement")
        exit(1)
    
    try:
        bot.run(TOKEN)
    except Exception as error:
        print(f"❌ Erreur lors du démarrage du bot: {error}")
