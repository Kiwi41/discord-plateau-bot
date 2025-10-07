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

// Test simple - juste pour la commande help
client.on('messageCreate', async (message) => {
    console.log(`📨 Message reçu: "${message.content}" de ${message.author.tag}`);
    
    if (message.author.bot) return;
    if (!message.member) return;
    
    if (message.content === '!plateau-help' || message.content === '!help') {
        const helpEmbed = new EmbedBuilder()
            .setTitle('🤖 Commandes Bot Soirées Plateaux')
            .setDescription('Commandes disponibles:')
            .addFields(
                { name: '!plateau-help', value: 'Affiche cette aide' },
                { name: '!test-simple', value: 'Test simple du bot' }
            )
            .setColor(0x7289DA)
            .setTimestamp();
        
        message.reply({ embeds: [helpEmbed] });
        return;
    }
    
    if (message.content === '!test-simple') {
        message.reply('✅ Bot fonctionnel ! Les corrections des liens ont été appliquées au code principal.');
        return;
    }
});

client.once('ready', () => {
    console.log(`🤖 Bot temporaire connecté en tant que ${client.user.tag}!`);
    console.log('✅ Les corrections de liens ont été appliquées avec succès');
    console.log('📝 Commandes disponibles: !plateau-help, !test-simple');
});

// Connexion du bot
client.login(config.token);