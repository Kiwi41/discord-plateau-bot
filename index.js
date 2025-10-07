require('dotenv').config();
const { Client, GatewayIntentBits, EmbedBuilder } = require('discord.js');
const cron = require('node-cron');

// Configuration du bot
const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent
    ]
});

// Configuration depuis les variables d'environnement
const config = {
    token: process.env.DISCORD_TOKEN,
    guildId: process.env.GUILD_ID,
    forumChannelId: process.env.FORUM_CHANNEL_ID,
    registrationUrl: process.env.REGISTRATION_URL || 'https://example.com/inscription',
    eventId: process.env.EVENT_ID,
    timezone: process.env.TIMEZONE || 'Europe/Paris'
};

// Fonction pour obtenir le prochain vendredi
function getNextFriday() {
    const now = new Date();
    const dayOfWeek = now.getDay(); // 0 = dimanche, 5 = vendredi, 6 = samedi
    const daysUntilFriday = (5 - dayOfWeek + 7) % 7;
    const nextFriday = new Date(now);
    
    if (dayOfWeek === 6) {
        // Si on est samedi, le prochain vendredi est dans 6 jours
        nextFriday.setDate(now.getDate() + 6);
    } else if (daysUntilFriday === 0 && now.getHours() >= 18) {
        // Si c'est vendredi après 18h, prendre le vendredi suivant
        nextFriday.setDate(now.getDate() + 7);
    } else {
        nextFriday.setDate(now.getDate() + (daysUntilFriday || 7));
    }
    
    return nextFriday;
}

// Fonction pour obtenir les 4 prochains vendredis
function getNextFourFridays() {
    const fridays = [];
    let currentFriday = getNextFriday();
    
    // Ajouter les 4 prochains vendredis
    for (let i = 0; i < 4; i++) {
        fridays.push(new Date(currentFriday));
        currentFriday.setDate(currentFriday.getDate() + 7); // Vendredi suivant
    }
    
    return fridays;
}

// Fonction pour formater la date en français
function formatDate(date) {
    const options = {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    };
    return date.toLocaleDateString('fr-FR', options);
}

// Fonction d'attente simple pour éviter les blocages
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Fonction pour trouver l'événement Discord du vendredi
function findFridayEvent(allEvents, targetDate) {
    try {
        console.log(`🔍 Recherche d'événements pour ${targetDate.toDateString()}...`);
        
        if (!allEvents) {
            console.log('⚠️  Aucun événement disponible, utilisation des valeurs par défaut');
            return null;
        }
        
        console.log(`📅 Recherche dans ${allEvents.size} événements`);
        
        // Chercher un événement qui correspond à la date du vendredi
        const fridayEvent = allEvents.find(event => {
            if (!event.scheduledStartAt) return false;
            
            const eventDate = new Date(event.scheduledStartAt);
            const targetDay = targetDate.toDateString();
            const eventDay = eventDate.toDateString();
            
            // Recherche plus flexible : plateau, soirée, jeu, etc.
            const eventName = event.name.toLowerCase();
            const keywords = ['plateau', 'soirée', 'jeu', 'board', 'game'];
            const hasKeyword = keywords.some(keyword => eventName.includes(keyword));
            
            return eventDay === targetDay && hasKeyword;
        });
        
        return fridayEvent;
    } catch (error) {
        console.warn('Erreur lors de la recherche d\'événements:', error.message);
        return null;
    }
}

// Fonction pour vérifier les doublons dans le forum
async function checkForDuplicates(forumChannel, postTitle) {
    try {
        // Récupérer les threads actifs du forum
        const activeThreads = await forumChannel.threads.fetchActive();
        const archivedThreads = await forumChannel.threads.fetchArchived();
        
        // Combiner tous les threads
        const allThreads = new Map([...activeThreads.threads, ...archivedThreads.threads]);
        
        // Chercher un thread avec le même titre
        for (const [threadId, thread] of allThreads) {
            if (thread.name === postTitle) {
                console.log(`⚠️  Post existant trouvé: ${thread.name} (ID: ${threadId})`);
                return thread;
            }
        }
        
        return null;
    } catch (error) {
        console.warn('Impossible de vérifier les doublons:', error.message);
        return null;
    }
}

// Fonction pour mettre à jour un post existant
async function updateExistingPost(thread, embed, eventInfo) {
    try {
        // Récupérer le premier message du thread (message principal)
        const messages = await thread.messages.fetch({ limit: 10 });
        const firstMessage = messages.last(); // Le dernier dans l'ordre chronologique = le premier posté
        
        if (!firstMessage || !firstMessage.author.bot) {
            console.log('❌ Impossible de trouver le message du bot à mettre à jour');
            return false;
        }
        
        // Vérifier si le contenu a changé en comparant les informations clés
        const currentEmbeds = firstMessage.embeds;
        if (currentEmbeds.length === 0) {
            console.log('🔄 Aucun embed trouvé, mise à jour du message');
            await firstMessage.edit({ embeds: [embed] });
            return true;
        }
        
        const currentEmbed = currentEmbeds[0];
        const currentFields = currentEmbed.fields || [];
        
        // Extraction des anciennes valeurs
        const oldTime = currentFields.find(f => f.name === '🕖 Heure')?.value || '';
        const oldLocation = currentFields.find(f => f.name === '📍 Lieu')?.value || '';
        
        // Comparaison avec les nouvelles valeurs
        const hasTimeChanged = oldTime !== eventInfo.time;
        const hasLocationChanged = oldLocation !== eventInfo.location;
        
        if (hasTimeChanged || hasLocationChanged) {
            console.log('🔄 Mise à jour détectée:');
            if (hasTimeChanged) console.log(`   🕖 Heure: "${oldTime}" → "${eventInfo.time}"`);
            if (hasLocationChanged) console.log(`   📍 Lieu: "${oldLocation}" → "${eventInfo.location}"`);
            
            await firstMessage.edit({ embeds: [embed] });
            return true;
        } else {
            console.log('✅ Aucune mise à jour nécessaire');
            return false;
        }
        
    } catch (error) {
        console.error('❌ Erreur lors de la mise à jour du post:', error);
        return false;
    }
}

// Fonction pour traiter un vendredi spécifique (création ou mise à jour)
async function processOneFriday(guild, forumChannel, fridayDate, allEvents = null) {
    const formattedDate = formatDate(fridayDate);
    const postTitle = `Soirée Plateaux - ${formattedDate}`;
    
    console.log(`📅 Traitement du ${formattedDate}...`);
    
    // Vérification des doublons
    const existingPost = await checkForDuplicates(forumChannel, postTitle);
    
    // Recherche de l'événement spécifique du vendredi
    console.log(`🔍 Recherche d'un événement spécifique pour ${formattedDate}...`);
    const fridayEvent = findFridayEvent(allEvents, fridayDate);
    console.log(`📋 Événement trouvé:`, fridayEvent ? `${fridayEvent.name} (ID: ${fridayEvent.id})` : 'Aucun');
    
    // Variables pour les informations de l'événement
    let eventDate, eventTime, eventLocation, eventUrl, eventText;
    let recurringEventData = null; // Pour stocker l'événement récurrent
    
    if (fridayEvent) {
        // Récupération des informations depuis l'événement Discord
        const eventStart = new Date(fridayEvent.scheduledStartAt);
        eventDate = formatDate(eventStart);
        
        // Formatage de l'heure avec timezone correcte
        eventTime = eventStart.toLocaleTimeString('fr-FR', { 
            hour: '2-digit', 
            minute: '2-digit',
            timeZone: config.timezone 
        });
        
        // Récupération du lieu selon le type d'événement
        if (fridayEvent.entityType === 3) { // EXTERNAL (événement externe)
            if (fridayEvent.entityMetadata?.location) {
                let location = fridayEvent.entityMetadata.location;
                
                // Nettoyer le lieu si c'est un lien Google Maps
                if (location.includes('https://www.google.com/maps')) {
                    // Extraire juste le nom du lieu (avant le " – " s'il existe)
                    const parts = location.split(' – ');
                    if (parts.length > 1) {
                        const placeName = parts[0].trim();
                        const mapUrl = parts[1].trim();
                        eventLocation = `📍 [${placeName}](${mapUrl})`;
                    } else {
                        eventLocation = `📍 ${location}`;
                    }
                } else {
                    eventLocation = `📍 ${location}`;
                }
            } else {
                eventLocation = 'Lieu externe (non spécifié)';
            }
        } else if (fridayEvent.entityType === 2) { // VOICE (canal vocal)
            if (fridayEvent.channel) {
                eventLocation = `🔊 ${fridayEvent.channel.name}`;
            } else {
                eventLocation = 'Canal vocal (non spécifié)';
            }
        } else if (fridayEvent.entityType === 1) { // STAGE_INSTANCE (scène)
            if (fridayEvent.channel) {
                eventLocation = `🎪 Scène: ${fridayEvent.channel.name}`;
            } else {
                eventLocation = 'Scène (non spécifiée)';
            }
        } else {
            eventLocation = 'Lieu à définir';
        }
        
        eventUrl = `https://discord.com/events/${config.guildId}/${fridayEvent.id}`;
        eventText = `[Rejoindre l'événement](${eventUrl})`;
        console.log(`✅ Événement spécifique trouvé: ${fridayEvent.name}`);
        console.log(`📅 Date de l'événement: ${eventDate}`);
        console.log(`🕖 Heure de l'événement: ${eventTime}`);
        console.log(`📍 Lieu de l'événement: ${eventLocation}`);
        
    } else if (config.eventId) {
        // Essayer de récupérer l'événement récurrent
        try {
            console.log(`🔍 Tentative de récupération de l'événement récurrent ID: ${config.eventId}`);
            
            // Ajouter un timeout pour éviter les blocages
            const timeoutPromise = new Promise((_, reject) => 
                setTimeout(() => reject(new Error('Timeout lors de la récupération de l\'événement récurrent')), 5000)
            );
            
            const recurringEvent = await Promise.race([
                guild.scheduledEvents.fetch(config.eventId),
                timeoutPromise
            ]);
            
            if (recurringEvent && recurringEvent.scheduledStartAt) {
                const eventStart = new Date(recurringEvent.scheduledStartAt);
                eventDate = formattedDate; // Garde la date calculée du vendredi
                eventTime = eventStart.toLocaleTimeString('fr-FR', { 
                    hour: '2-digit', 
                    minute: '2-digit',
                    timeZone: config.timezone 
                });
                
                // Récupération du lieu selon le type d'événement récurrent
                if (recurringEvent.entityType === 3) { // EXTERNAL
                    if (recurringEvent.entityMetadata?.location) {
                        let location = recurringEvent.entityMetadata.location;
                        
                        // Nettoyer le lieu si c'est un lien Google Maps
                        if (location.includes('https://www.google.com/maps')) {
                            const parts = location.split(' – ');
                            if (parts.length > 1) {
                                const placeName = parts[0].trim();
                                const mapUrl = parts[1].trim();
                                eventLocation = `📍 [${placeName}](${mapUrl})`;
                            } else {
                                eventLocation = `📍 ${location}`;
                            }
                        } else {
                            eventLocation = `📍 ${location}`;
                        }
                    } else {
                        eventLocation = 'Lieu externe (non spécifié)';
                    }
                } else if (recurringEvent.entityType === 2) { // VOICE
                    if (recurringEvent.channel) {
                        eventLocation = `🔊 ${recurringEvent.channel.name}`;
                    } else {
                        eventLocation = 'Canal vocal (non spécifié)';
                    }
                } else if (recurringEvent.entityType === 1) { // STAGE_INSTANCE
                    if (recurringEvent.channel) {
                        eventLocation = `🎪 Scène: ${recurringEvent.channel.name}`;
                    } else {
                        eventLocation = 'Scène (non spécifiée)';
                    }
                } else {
                    eventLocation = 'Lieu à définir';
                }
                
                eventUrl = `https://discord.com/events/${config.guildId}/${config.eventId}`;
                eventText = `[Rejoindre l'événement Discord](${eventUrl})`;
                recurringEventData = recurringEvent; // Stocker pour utiliser la description
                console.log('✅ Événement récurrent récupéré avec succès');
                
            } else {
                console.log('⚠️  Événement récurrent trouvé mais sans date de début');
                eventDate = formattedDate;
                eventTime = '20:30'; // Utilise l'heure de l'événement du 10 octobre
                eventLocation = '📍 [Le Cube en Bois](https://www.google.com/maps/place/Le+D%C3%A9mon+du+Jeu/@47.6239545,1.3247093,214m)';
                eventUrl = `https://discord.com/events/${config.guildId}/${config.eventId}`;
                eventText = `[Rejoindre l'événement Discord](${eventUrl})`;
            }
        } catch (error) {
            console.warn('❌ Impossible de récupérer l\'événement récurrent:', error.message);
            console.log('🔄 Utilisation des valeurs par défaut');
            eventDate = formattedDate;
            eventTime = '20:30'; // Heure par défaut basée sur le pattern observé
            eventLocation = '📍 [Le Cube en Bois](https://www.google.com/maps/place/Le+D%C3%A9mon+du+Jeu/@47.6239545,1.3247093,214m)'; // Lieu avec lien Google Maps
            
            // Utiliser l'événement récurrent si disponible, sinon lien d'inscription
            if (config.eventId) {
                eventUrl = `https://discord.com/events/${config.guildId}/${config.eventId}`;
                eventText = `[Rejoindre l'événement Discord](${eventUrl})`;
            } else {
                eventUrl = config.registrationUrl;
                eventText = `[Lien d'inscription](${eventUrl})`;
            }
        }
        
        console.log('⚠️  Utilisation de l\'événement récurrent ou des valeurs par défaut');
    } else {
        // Pas d'événement spécifique trouvé, chercher un événement récurrent des soirées plateaux
        console.log('🔍 Recherche d\'un événement récurrent des soirées plateaux...');
        let recurringEvent = null;
        
        if (allEvents && allEvents.size > 0) {
            // Chercher un événement récurrent avec des mots-clés pertinents
            recurringEvent = allEvents.find(event => {
                const eventName = event.name.toLowerCase();
                const keywords = ['plateau', 'soirée', 'récurrent', 'hebdomadaire', 'vendredi'];
                const hasKeyword = keywords.some(keyword => eventName.includes(keyword));
                return hasKeyword && event.scheduledStartAt;
            });
            
            if (recurringEvent) {
                console.log(`✅ Événement récurrent trouvé: ${recurringEvent.name} (ID: ${recurringEvent.id})`);
                
                // Utiliser les informations de l'événement récurrent
                const eventStart = new Date(recurringEvent.scheduledStartAt);
                eventDate = formattedDate; // Garde la date calculée du vendredi
                eventTime = eventStart.toLocaleTimeString('fr-FR', { 
                    hour: '2-digit', 
                    minute: '2-digit',
                    timeZone: config.timezone 
                });
                
                // Récupération du lieu selon le type d'événement
                if (recurringEvent.entityType === 3) { // EXTERNAL
                    if (recurringEvent.entityMetadata?.location) {
                        let location = recurringEvent.entityMetadata.location;
                        if (location.includes('https://www.google.com/maps')) {
                            const parts = location.split(' – ');
                            if (parts.length > 1) {
                                const placeName = parts[0].trim();
                                const mapUrl = parts[1].trim();
                                eventLocation = `📍 [${placeName}](${mapUrl})`;
                            } else {
                                eventLocation = `📍 ${location}`;
                            }
                        } else {
                            eventLocation = `📍 ${location}`;
                        }
                    } else {
                        eventLocation = 'Lieu externe (non spécifié)';
                    }
                } else if (recurringEvent.entityType === 2) { // VOICE
                    if (recurringEvent.channel) {
                        eventLocation = `🔊 ${recurringEvent.channel.name}`;
                    } else {
                        eventLocation = 'Canal vocal (non spécifié)';
                    }
                } else {
                    eventLocation = '📍 [Le Cube en Bois](https://www.google.com/maps/place/Le+D%C3%A9mon+du+Jeu/@47.6239545,1.3247093,214m)';
                }
                
                eventUrl = `https://discord.com/events/${config.guildId}/${recurringEvent.id}`;
                eventText = `[Rejoindre l'événement Discord](${eventUrl})`;
                recurringEventData = recurringEvent; // Stocker pour utiliser la description
                console.log('✅ Utilisation des informations de l\'événement récurrent trouvé');
            }
        }
        
        // Si aucun événement récurrent trouvé, utiliser les valeurs par défaut
        if (!recurringEvent) {
            eventDate = formattedDate;
            eventTime = '20:30'; // Heure cohérente basée sur les autres événements
            eventLocation = '📍 [Le Cube en Bois](https://www.google.com/maps/place/Le+D%C3%A9mon+du+Jeu/@47.6239545,1.3247093,214m)';
            
            // Utiliser l'événement récurrent si EVENT_ID configuré, sinon lien d'inscription
            if (config.eventId) {
                eventUrl = `https://discord.com/events/${config.guildId}/${config.eventId}`;
                eventText = `[Rejoindre l'événement Discord](${eventUrl})`;
                console.log('⚠️  Utilisation du lien vers l\'événement récurrent configuré');
            } else {
                eventUrl = config.registrationUrl;
                eventText = `[Lien d'inscription](${eventUrl})`;
                console.log('⚠️  Utilisation de l\'URL d\'inscription générique');
            }
        }
    }
    
    // Description de l'embed (priorité: événement spécifique > événement récurrent > description par défaut)
    let embedDescription = 'Rejoignez-nous pour une soirée jeux de plateau conviviale !';
    
    if (fridayEvent && fridayEvent.description && fridayEvent.description.trim()) {
        // Utiliser la description de l'événement spécifique du vendredi
        embedDescription = fridayEvent.description;
        console.log('📝 Utilisation de la description de l\'événement spécifique');
    } else if (recurringEventData && recurringEventData.description && recurringEventData.description.trim()) {
        // Utiliser la description de l'événement récurrent
        embedDescription = recurringEventData.description;
        console.log('📝 Utilisation de la description de l\'événement récurrent');
    } else {
        // Description par défaut améliorée
        embedDescription = `🎲 **Soirée Plateaux du vendredi !**

Venez découvrir et jouer à une grande variété de jeux de plateau dans une ambiance conviviale !

🎯 **Au programme :**
• Jeux de stratégie, coopératifs, party games...
• Accueil des débutants et confirmés
• Ambiance détendue et bonne humeur garantie

**Rendez-vous ${eventTime} pour une soirée inoubliable !** 🎉`;
        console.log('📝 Utilisation de la description par défaut');
    }
    
    // Création de l'embed pour le message
    const embed = new EmbedBuilder()
        .setTitle('🎲 Soirée Plateaux du Vendredi ! 🎲')
        .setDescription(embedDescription)
        .addFields(
            { name: '📅 Date', value: eventDate, inline: true },
            { name: '🕖 Heure', value: eventTime, inline: true },
            { name: '📍 Lieu', value: eventLocation, inline: true },
            { name: '🎯 Événement Discord', value: eventText, inline: false }
        )
        .setColor(0x7289DA)
        .setTimestamp()
        .setFooter({ text: 'Bot Soirées Plateaux' });
    
    // Informations pour la comparaison de mise à jour
    const eventInfo = {
        date: eventDate,
        time: eventTime,
        location: eventLocation
    };
    
    if (existingPost) {
        // Post existant - vérifier s'il faut le mettre à jour
        const wasUpdated = await updateExistingPost(existingPost, embed, eventInfo);
        if (wasUpdated) {
            console.log(`🔄 Post mis à jour: ${postTitle}`);
            return { action: 'updated', thread: existingPost };
        } else {
            console.log(`✅ Post déjà à jour: ${postTitle}`);
            return { action: 'unchanged', thread: existingPost };
        }
    } else {
        // Créer un nouveau post
        try {
            const thread = await forumChannel.threads.create({
                name: postTitle,
                message: { embeds: [embed] }
            });
            
            console.log(`✅ Nouveau post créé: ${postTitle}`);
            console.log(`🔗 Lien: https://discord.com/channels/${config.guildId}/${thread.id}`);
            return { action: 'created', thread: thread };
        } catch (error) {
            console.error(`❌ Erreur lors de la création du post pour ${formattedDate}:`, error);
            return { action: 'error', error: error };
        }
    }
}

// Fonction pour créer/mettre à jour les 4 prochains vendredis
async function processNextFourFridays() {
    try {
        console.log('🔄 Traitement des 4 prochains vendredis...');
        
        const guild = client.guilds.cache.get(config.guildId);
        if (!guild) {
            console.error('Serveur Discord non trouvé');
            return;
        }

        const forumChannel = guild.channels.cache.get(config.forumChannelId);
        if (!forumChannel) {
            console.error('Canal forum non trouvé');
            return;
        }

        // Obtenir les 4 prochains vendredis
        const fridays = getNextFourFridays();
        console.log(`📅 Les 4 prochains vendredis à traiter:`);
        fridays.forEach((friday, index) => {
            console.log(`   ${index + 1}. ${formatDate(friday)}`);
        });
        
        // Récupérer tous les événements une seule fois au début pour éviter les blocages
        console.log('🔍 Récupération des événements Discord...');
        let allEvents = null;
        try {
            const timeoutPromise = new Promise((_, reject) => 
                setTimeout(() => reject(new Error('Timeout lors de la récupération des événements')), 10000)
            );
            
            allEvents = await Promise.race([
                guild.scheduledEvents.fetch(),
                timeoutPromise
            ]);
            console.log(`📅 ${allEvents.size} événements trouvés sur le serveur`);
        } catch (error) {
            console.warn('⚠️  Impossible de récupérer les événements Discord:', error.message);
            console.log('🔄 Le traitement continuera avec les valeurs par défaut');
        }

        const results = {
            created: 0,
            updated: 0,
            unchanged: 0,
            errors: 0
        };
        
        // Traiter chaque vendredi
        for (let i = 0; i < fridays.length; i++) {
            const friday = fridays[i];
            console.log(`\n🔄 Traitement ${i + 1}/4: ${formatDate(friday)}`);
            
            try {
                console.log(`🚀 Début du traitement pour ${formatDate(friday)}...`);
                const result = await processOneFriday(guild, forumChannel, friday, allEvents);
                console.log(`✅ Fin du traitement pour ${formatDate(friday)}`);
                
                console.log(`📊 Résultat pour ${formatDate(friday)}: ${result.action}`);
                
                switch (result.action) {
                    case 'created':
                        results.created++;
                        break;
                    case 'updated':
                        results.updated++;
                        break;
                    case 'unchanged':
                        results.unchanged++;
                        break;
                    case 'error':
                        results.errors++;
                        console.error(`❌ Erreur pour ${formatDate(friday)}:`, result.error);
                        break;
                }
                
                // Petite pause entre chaque traitement pour éviter les rate limits
                if (i < fridays.length - 1) {
                    console.log(`⏳ Pause de 2 secondes avant le vendredi suivant...`);
                    await sleep(2000);
                    console.log(`✅ Fin de pause, continuons avec le vendredi suivant...`);
                }
                
            } catch (error) {
                console.error(`❌ Erreur lors du traitement de ${formatDate(friday)}:`, error);
                console.error(`🔍 Stack trace:`, error.stack);
                results.errors++;
                
                // Même en cas d'erreur, on continue avec les autres vendredis
                if (i < fridays.length - 1) {
                    console.log(`⏳ Pause de 2 secondes après l'erreur...`);
                    await sleep(2000);
                }
            }
        }
        
        // Résumé final
        console.log('\n📋 Résumé du traitement:');
        console.log(`   ✅ ${results.created} posts créés`);
        console.log(`   🔄 ${results.updated} posts mis à jour`);
        console.log(`   ⚪ ${results.unchanged} posts inchangés`);
        console.log(`   ❌ ${results.errors} erreurs`);
        
    } catch (error) {
        console.error('❌ Erreur lors du traitement des posts:', error);
    }
}

// Fonction pour traiter uniquement le prochain vendredi (ancienne fonction)
async function createForumPost() {
    try {
        console.log('Tentative de création du post pour le prochain vendredi...');
        
        const guild = client.guilds.cache.get(config.guildId);
        if (!guild) {
            console.error('Serveur Discord non trouvé');
            return;
        }

        const forumChannel = guild.channels.cache.get(config.forumChannelId);
        if (!forumChannel) {
            console.error('Canal forum non trouvé');
            return;
        }

        const nextFriday = getNextFriday();
        const result = await processOneFriday(guild, forumChannel, nextFriday);
        
        if (result.action === 'error') {
            console.error('❌ Erreur lors du traitement:', result.error);
        }
        
    } catch (error) {
        console.error('❌ Erreur lors de la création du post:', error);
    }
}

// Événement quand le bot est prêt
client.once('clientReady', () => {
    console.log(`🤖 Bot connecté en tant que ${client.user.tag}!`);
    console.log(`📊 Serveurs: ${client.guilds.cache.size}`);
    console.log(`👥 Utilisateurs: ${client.users.cache.size}`);
    
    // Afficher les serveurs où le bot est présent
    console.log('🏠 Serveurs où le bot est présent:');
    client.guilds.cache.forEach(guild => {
        console.log(`   - ${guild.name} (ID: ${guild.id})`);
    });
    
    console.log('🕒 Planification active: Samedis à 3h00 (Europe/Paris)');
    console.log('📝 Commandes manuelles:');
    console.log('   - !create-plateau-post (prochain vendredi)');
    console.log('   - !process-next-month (4 prochains vendredis)');
    console.log('   - !plateau-help (aide)');
});

// Planification automatique: tous les samedis à 3h00 du matin
// Cela créera/mettra à jour les posts pour les 4 prochains vendredis
// Format cron: 'minute heure * * jour_semaine' (0=dimanche, 6=samedi)
cron.schedule('0 3 * * 6', () => {
    console.log('⏰ Tâche planifiée déclenchée - Traitement des 4 prochains vendredis (Samedi 3h00)');
    processNextFourFridays();
}, {
    scheduled: true,
    timezone: config.timezone
});

// Test de réception de messages (pour diagnostiquer)
client.on('messageCreate', async (message) => {
    console.log(`📨 Message reçu: "${message.content}" de ${message.author.tag} dans ${message.guild?.name || 'DM'}`);
    
    if (message.author.bot) {
        console.log('🤖 Message ignoré: provient d\'un bot');
        return;
    }
    
    // Test simple - répondre à n'importe quel message qui commence par !test
    if (message.content === '!test') {
        console.log('🧪 Test de réponse...');
        message.reply('✅ Le bot reçoit bien les messages !');
        return;
    }
    
    if (!message.member) {
        console.log('❌ Message ignoré: pas de membre (message privé?)');
        return;
    }
    
    console.log(`👤 Utilisateur: ${message.author.tag}, Admin: ${message.member.permissions.has('Administrator')}`);
    
    // TEMPORAIRE: Permettre à tous les utilisateurs pour les tests
    // if (!message.member.permissions.has('Administrator')) {
    //     console.log('❌ Message ignoré: utilisateur non administrateur');
    //     return;
    // }
    
    console.log('✅ Utilisateur autorisé, traitement de la commande...');
    
    // Commande pour créer/mettre à jour un post pour le prochain vendredi
    if (message.content === '!create-plateau-post') {
        message.reply('🔄 Création/mise à jour du post pour le prochain vendredi...');
        await createForumPost();
        message.channel.send('✅ Traitement terminé!');
    }
    
    // Commande pour traiter les 4 prochains vendredis
    if (message.content === '!process-next-month' || message.content === '!plateau-next-month') {
        message.reply('📅 Traitement des 4 prochains vendredis en cours...');
        await processNextFourFridays();
        message.channel.send('✅ Traitement des 4 prochains vendredis terminé!');
    }
    
    // Commande d'aide
    if (message.content === '!plateau-help') {
        const helpEmbed = new EmbedBuilder()
            .setTitle('🤖 Commandes Bot Soirées Plateaux')
            .setDescription('Commandes disponibles:')
            .addFields(
                { name: '!create-plateau-post', value: 'Crée ou met à jour le post pour le prochain vendredi' },
                { name: '!process-next-month', value: 'Traite les 4 prochains vendredis (création + mise à jour)' },
                { name: '!plateau-next-month', value: 'Alias pour !process-next-month' },
                { name: '!plateau-help', value: 'Affiche cette aide' }
            )
            .setColor(0x7289DA)
            .setTimestamp();
        
        message.reply({ embeds: [helpEmbed] });
    }
});

// Gestion des erreurs
process.on('unhandledRejection', error => {
    console.error('❌ Erreur non gérée:', error);
});

client.on('error', error => {
    console.error('❌ Erreur Discord.js:', error);
});

// Connexion du bot
if (!config.token) {
    console.error('❌ ERREUR: Token Discord manquant dans les variables d\'environnement');
    process.exit(1);
}

client.login(config.token);