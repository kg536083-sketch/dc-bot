require('dotenv').config();
const { Client, GatewayIntentBits, Partials, Collection } = require('discord.js');
const { LavalinkManager } = require('lavalink-client');
const axios = require('axios');

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent,
        GatewayIntentBits.GuildVoiceStates
    ]
});

// -------- Lavalink Setup (Bypasses local Opus requirements) -------- #
// THE MOST ROBUST TECHNOLOGY FOR DISCORD MUSIC - 0% LOCAL PROCESSING
const nodes = [
    {
        host: "lavalink.lexis.host",
        port: 443,
        password: "lexishostlavalink",
        secure: true
    }
];

client.lavalink = new LavalinkManager({
    nodes: nodes,
    sendToShard: (guildId, payload) => {
        client.guilds.cache.get(guildId)?.shard?.send(payload);
    },
    client: {
        id: "", // Will be auto-set on ready
        username: "Homeless Girl"
    }
});

// -------- Slash Commands -------- #

client.on("interactionCreate", async (interaction) => {
    if (!interaction.isChatInputCommand()) return;

    if (interaction.commandName === "play") {
        const query = interaction.options.getString("query");
        if (!interaction.member.voice.channel) return interaction.reply("❌ Join a voice channel first!");

        await interaction.deferReply();

        let player = client.lavalink.getPlayer(interaction.guildId);
        if (!player) {
            player = await client.lavalink.createPlayer({
                guildId: interaction.guildId,
                voiceChannelId: interaction.member.voice.channelId,
                textChannelId: interaction.channelId,
                selfDeaf: true
            });
        }

        if (!player.connected) await player.connect();

        const res = await player.search({ query: query }, interaction.user);
        if (!res.tracks.length) return interaction.followup("❌ No tracks found, baby. 🥺");

        const track = res.tracks[0];
        player.queue.add(track);

        if (!player.playing) await player.play();
        await interaction.followup(`🎶 Now playing: **${track.info.title}**`);
    }

    if (interaction.commandName === "stop") {
        const player = client.lavalink.getPlayer(interaction.guildId);
        if (player) {
            await player.destroy();
            await interaction.reply("⏹️ Stopped everything and left! 👋");
        } else {
            await interaction.reply("❌ I'm not playing anything right now.");
        }
    }

    if (interaction.commandName === "skip") {
        const player = client.lavalink.getPlayer(interaction.guildId);
        if (player && player.playing) {
            await player.skip();
            await interaction.reply("⏭️ Skipped to the next one!");
        } else {
            await interaction.reply("❌ Nothing to skip!");
        }
    }
});

// -------- Crypto Prices (CoinGecko) -------- #

async function getCryptoPrice(query) {
    try {
        const r = await axios.get(`https://api.coingecko.com/api/v3/search?query=${query}`);
        if (r.data.coins && r.data.coins.length > 0) {
            const coinId = r.data.coins[0].id;
            const p = await axios.get(`https://api.coingecko.com/api/v3/coins/${coinId}?localization=false&tickers=false&market_data=true`);
            const md = p.data.market_data;
            const price = md.current_price.usd || "N/A";
            const change = md.price_change_percentage_24h || "N/A";
            return `**${p.data.name} (${p.data.symbol.toUpperCase()})**\n💰 **Price:** $${price} USD\n📅 **24h Change:** ${change}%`;
        }
    } catch (e) {}
    return `I couldn't find any crypto data for \`${query}\`.`;
}

// -------- AI Chat (Groq) -------- #

async function aiReply(message) {
    const url = "https://api.groq.com/openai/v1/chat/completions";
    const headers = { "Authorization": `Bearer ${process.env.GROQ_API_KEY}`, "Content-Type": "application/json" };
    const data = {
        model: "llama-3.1-8b-instant",
        messages: [
            { role: "system", content: "You are Homeless Girl, a playful, flirty girl chatting in Discord. Speak casually with sweet words like baby, darling, sweetheart. Keep it short and cute." },
            { role: "user", content: `${message.author.displayName} says: ${message.content}` }
        ],
        temperature: 1, max_tokens: 100
    };
    try {
        const r = await axios.post(url, data, { headers });
        return r.data.choices[0].message.content;
    } catch (e) {
        return "Oops! I'm having a little brain freeze, baby. 🧊";
    }
}

// -------- Events -------- #

client.on("ready", async () => {
    client.lavalink.options.client.id = client.user.id;
    await client.application.commands.set([
        { name: "play", description: "Play music (Opus-free tech!)", options: [{ name: "query", type: 3, description: "Song name or URL", required: true }] },
        { name: "stop", description: "Stop the bot and leave" },
        { name: "skip", description: "Skip current song" }
    ]);
    console.log(`[READY] ${client.user.tag} is online and Opus-free!`);
});

client.on("messageCreate", async (message) => {
    if (message.author.bot) return;
    const text = message.content.toLowerCase();

    // Check for $token
    if (text.includes("$")) {
        const match = text.match(/\$([a-zA-Z]+)/);
        if (match) return message.reply(await getCryptoPrice(match[1]));
    }

    // AI Chat
    if (text.includes("homeless girl") || message.mentions.has(client.user)) {
        return message.reply(await aiReply(message));
    }
});

// Sync voice state with Lavalink
client.on("raw", (d) => client.lavalink.sendRawData(d));

client.login(process.env.DISCORD_TOKEN);
