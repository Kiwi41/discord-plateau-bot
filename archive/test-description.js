mrequire('dotenv').config();
const { Client, GatewayIntentBits, EmbedBuilder } = require('discord.js');

// Configuration du bot
const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent
    ]
});

const config = {
    token: process.env.DISCORD_TOKEN,
    guildId: process.env.GUILD_ID,
    forumChannelId: process.env.FORUM_CHANNEL_ID,
    registrationUrl: process.env.REGISTRATION_URL || 'https://example.com/inscription',
    eventId: process.env.EVENT_ID,
    timezone: process.env.TIMEZONE || 'Europe/Paris'
};

client.on('messageCreate', async (message) => {
    if (message.author.bot) return;
    if (!message.member) return;
    
    if (message.content === '!test-description') {
        console.log('🧪 Test de la nouvelle description...');
        
        // Simuler un événement sans description spécifique
        const eventDate = 'vendredi 17 octobre 2025';
        const eventTime = '20:30';
        const eventLocation = '📍 [Le Cube en Bois](https://www.google.com/maps/place/Le+D%C3%A9mon+du+Jeu/@47.6239545,1.3247093,214m)';
        const eventText = `[Rejoindre l'événement Discord](https://discord.com/events/${config.guildId}/${config.eventId})`;
        
        // Description améliorée
        const embedDescription = `🎲 **Soirée Plateaux du vendredi !**

Venez découvrir et jouer à une grande variété de jeux de plateau dans une ambiance conviviale !

🎯 **Au programme :**
• Jeux de stratégie, coopératifs, party games...
• Accueil des débutants et confirmés
• Ambiance détendue et bonne humeur garantie

**Rendez-vous ${eventTime} pour une soirée inoubliable !** 🎉`;

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

        message.reply({ embeds: [embed] });
        return;
    }
    
    if (message.content === '!help') {
        message.reply('Commandes: !test-description, !help');
        return;
    }
});

client.once('ready', () => {
    console.log(`🤖 Bot test description connecté en tant que ${client.user.tag}!`);
    console.log('📝 Tapez !test-description pour voir la nouvelle description');
});

client.login(config.token);