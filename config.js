class DiscordBotConfig {
    constructor() {
        this.validateEnvironment();
    }
    
    validateEnvironment() {
        const required = ['DISCORD_TOKEN', 'GUILD_ID', 'FORUM_CHANNEL_ID'];
        const missing = required.filter(key => !process.env[key]);
        
        if (missing.length > 0) {
            throw new Error(`Variables d'environnement manquantes: ${missing.join(', ')}`);
        }
    }
    
    get token() {
        return process.env.DISCORD_TOKEN;
    }
    
    get guildId() {
        return process.env.GUILD_ID;
    }
    
    get forumChannelId() {
        return process.env.FORUM_CHANNEL_ID;
    }
    
    get registrationUrl() {
        return process.env.REGISTRATION_URL || 'https://example.com/inscription';
    }
    
    get timezone() {
        return process.env.TIMEZONE || 'Europe/Paris';
    }
}

module.exports = DiscordBotConfig;