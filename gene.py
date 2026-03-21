import discord
from discord import app_commands
import requests
import os
import re
import asyncio
import yt_dlp

TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_KEY = os.getenv("GROQ_API_KEY")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# -------- Music Source Setup -------- #

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn',
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_query(cls, query, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(f"ytsearch:{query}", download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        import imageio_ffmpeg
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        return cls(discord.FFmpegPCMAudio(filename, executable=ffmpeg_exe, **ffmpeg_options), data=data)

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        import imageio_ffmpeg
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        return cls(discord.FFmpegPCMAudio(filename, executable=ffmpeg_exe, **ffmpeg_options), data=data)

# -------- Slash Commands for Music -------- #

@tree.command(name="play", description="Play a song or use 'music' for random music")
async def play(interaction: discord.Interaction, query: str):
    if not interaction.guild:
        await interaction.response.send_message("❌ You must use this command in a server!")
        return

    TARGET_CHANNEL_ID = 1467485300791181333
    channel = client.get_channel(TARGET_CHANNEL_ID)
    
    if not channel:
        try:
            channel = await client.fetch_channel(TARGET_CHANNEL_ID)
        except:
            await interaction.response.send_message("❌ Couldn't find the target streaming channel!")
            return

    voice_client = interaction.guild.voice_client

    if voice_client is None:
        voice_client = await channel.connect()
    elif voice_client.channel != channel:
        await voice_client.move_to(channel)

    await interaction.response.defer()

    if query.lower() == "music":
        URL = "https://www.twitch.tv/lofigirl" # Lofi Girl Radio on Twitch (Bypasses YouTube blocks)
        try:
            player = await YTDLSource.from_url(URL, loop=client.loop, stream=True)
            if voice_client.is_playing():
                voice_client.stop()
            voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
            await interaction.followup.send("🎶 Now playing: **Random streaming music (Lofi radio)** 🎧")
        except Exception as e:
            import traceback
            traceback.print_exc()
            await interaction.followup.send(f"❌ An error occurred while trying to play random music: `{e.__class__.__name__}: {str(e)}`")
        return

    try:
        player = await YTDLSource.from_query(query, loop=client.loop, stream=True)
        if voice_client.is_playing():
            voice_client.stop()
        voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
        await interaction.followup.send(f"🎶 Now playing: **{player.title}**")
    except Exception as e:
        import traceback
        traceback.print_exc()
        await interaction.followup.send(f"❌ An error occurred: `{e.__class__.__name__}: {str(e)}`")

@tree.command(name="stop", description="Stop the music and leave")
async def stop(interaction: discord.Interaction):
    if not interaction.guild:
        await interaction.response.send_message("❌ You must use this command in a server!")
        return

    voice_client = interaction.guild.voice_client
    if voice_client:
        await voice_client.disconnect()
        await interaction.response.send_message("⏹️ Stopped the music and left the channel.")
    else:
        await interaction.response.send_message("❌ I'm not in a voice channel.")

# -------- Crypto APIs -------- #
# -------- Crypto APIs -------- #

def get_crypto_price(query):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    # Primary: CoinGecko (Upgraded to fetch Full Data including FDV)
    try:
        r = requests.get(f"https://api.coingecko.com/api/v3/search?query={query}", headers=headers).json()
        if r.get("coins"):
            coin_id = r["coins"][0]["id"]
            
            p = requests.get(f"https://api.coingecko.com/api/v3/coins/{coin_id}?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false", headers=headers).json()
            if "market_data" in p:
                md = p["market_data"]
                name = p.get("name", query.title())
                symbol = p.get("symbol", query).upper()
                rank = p.get("market_cap_rank", "N/A")
                
                usd_price = md.get("current_price", {}).get("usd", "N/A")
                if isinstance(usd_price, (int, float)):
                    usd_price = round(usd_price, 4) if usd_price > 0.0001 else usd_price
                
                market_cap = md.get("market_cap", {}).get("usd", "N/A")
                if isinstance(market_cap, (int, float)) and market_cap > 0: market_cap = f"${int(market_cap):,}"
                else: market_cap = "N/A"
                
                fdv = md.get("fully_diluted_valuation", {}).get("usd", "N/A")
                if isinstance(fdv, (int, float)) and fdv > 0: fdv = f"${int(fdv):,}"
                else: fdv = "N/A"
                
                change = md.get("price_change_percentage_24h", "N/A")
                if isinstance(change, (int, float)): change = round(change, 2)
                
                info = f"**{name} ({symbol})** (Rank: {rank})\n"
                info += f"💰 **Price:** ${usd_price} USD\n"
                if market_cap != "N/A": info += f"📊 **Market Cap:** {market_cap}\n"
                if fdv != "N/A": info += f"📈 **FDV:** {fdv}\n"
                info += f"📅 **24h Change:** {change}%\n"
                return info
    except Exception as e:
        print(f"CoinGecko Error fetching price: {e}", flush=True)

    # Fallback: CoinMarketCap (Full Data Backup)
    try:
        symbol_query = query.upper()
        lower_query = query.lower()
        
        m_name = symbol_query
        m_rank = "N/A"
        slug = None

        m_res = requests.get('https://api.coinmarketcap.com/data-api/v3/map/all?cryptoAux=is_active,status', headers=headers, timeout=5).json()
        for p in m_res.get("data", {}).get("cryptoCurrencyMap", []):
            if (p["symbol"].upper() == symbol_query or p["slug"].lower() == lower_query or p["name"].lower() == lower_query) and p.get("status") == "active":
                slug = p["slug"]
                m_name = p["name"]
                m_rank = p.get("rank", "N/A")
                break
                
        if slug:
            c_res = requests.get(f"https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail?slug={slug}", headers=headers).json()
            if "data" in c_res and "statistics" in c_res["data"]:
                stats = c_res["data"]["statistics"]
                usd_price = stats.get("price", "N/A")
                if isinstance(usd_price, (int, float)):
                    usd_price = round(usd_price, 4) if usd_price > 0.0001 else usd_price
                    
                change = stats.get("priceChangePercentage24h", "N/A")
                if isinstance(change, (int, float)): change = round(change, 2)
                
                market_cap = stats.get("marketCap", "N/A")
                if isinstance(market_cap, (int, float)) and market_cap > 0: market_cap = f"${int(market_cap):,}"
                else: market_cap = "N/A"
                
                fdv = stats.get("fullyDilutedMarketCap", "N/A")
                if isinstance(fdv, (int, float)) and fdv > 0: fdv = f"${int(fdv):,}"
                else: fdv = "N/A"
                
                info = f"**{m_name} ({symbol_query})** (Rank: {m_rank})\n"
                info += f"💰 **Price:** ${usd_price} USD\n"
                if market_cap != "N/A": info += f"📊 **Market Cap:** {market_cap}\n"
                if fdv != "N/A": info += f"📈 **FDV:** {fdv}\n"
                info += f"📅 **24h Change:** {change}%\n"
                return info
    except Exception as e:
        print(f"CoinMarketCap Error fetching price: {e}", flush=True)

    return f"I couldn't find any data for `{query}`! (The APIs might be blocked or the coin doesn't exist.)"

def get_crypto_news():
    try:
        r = requests.get("https://min-api.cryptocompare.com/data/v2/news/?lang=EN").json()
        news = r.get("Data", [])[:6]
        if news:
            headlines = [f"• {n['title']}" for n in news]
            return "**Latest Crypto News (Top 6):**\n" + "\n".join(headlines)
    except Exception as e:
        print(f"Error fetching news: {e}", flush=True)
    return "I couldn't fetch the news right now!"

# -------- AI reply using Groq -------- #

def ai_reply(message):

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_KEY}",
        "Content-Type": "application/json"
    }
    
    context = []
    
    if message.mentions:
        mentions_info = "Here are the users mentioned natively. If asked to tag/mention them, USE EXACTLY their Tag Format:\n"
        for user in message.mentions:
            if user != client.user:
                mentions_info += f"- Name: {user.display_name}, Tag Format: <@{user.id}>\n"
        context.append(mentions_info)
        
    context.append(f"{message.author.display_name} (Tag: <@{message.author.id}>) says: {message.content}")
    user_content = "\n".join(context)

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": "You are Homeless Girl, a playful flirty girl chatting in a Discord server. Speak casually and affectionately using words like baby, darling, sweetheart, love and handsome. Keep replies short and playful. IMPORTANT RULES: 1) You are ALLOWED to mention a user if explicitly requested. When tagging someone, you MUST use their absolute exact Tag Format (e.g. <@12345678>). 2) NEVER tag yourself."
            },
            {
                "role": "user",
                "content": user_content
            }
        ],
        "temperature": 1,
        "max_tokens": 150
    }

    try:
        r = requests.post(url, headers=headers, json=data)
        if r.status_code != 200:
            print(f"Groq API Error: {r.status_code} - {r.text}", flush=True)
            return "Oops! I'm having a little brain freeze right now. 🧊"
        
        result = r.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error in ai_reply: {e}", flush=True)
        return "Oops! I couldn't think of a reply right now, baby. 🥺"

# -------- Discord events -------- #

@client.event
async def on_ready():
    await tree.sync()
    print(f"Homeless Girl is online as {client.user}", flush=True)

@client.event
async def on_message(message):
    print(f"[DEBUG] Event triggered by {message.author}", flush=True)

    if message.author == client.user:
        return

    text = message.content.lower()

    print(f"[DEBUG] Received message from {message.author}: '{text}'", flush=True)

    trigger_words = ["homeless girl", "ping", "tag", "mention", "hey homeless girl"]

    is_directed_at_bot = any(word in text for word in trigger_words) or client.user in message.mentions
    has_token = bool(re.search(r'\$([a-zA-Z]+[a-zA-Z0-9\-]*)', text))
    has_news = "news" in text and is_directed_at_bot
    has_price = "price" in text and is_directed_at_bot

    # Handle crypto-specific commands (Bypass AI entirely)
    if has_token or has_price:
        queries = []
        token_matches = re.findall(r'\$([a-zA-Z]+[a-zA-Z0-9\-]*)', text)
        queries.extend(token_matches)
        
        if not queries and is_directed_at_bot:
            price_match = re.search(r'price\s+(?:of|for)?\s*([a-zA-Z0-9\-]+)', text)
            if price_match:
                queries.append(price_match.group(1))

        if queries:
            replies = []
            for query in set(queries):
                replies.append(get_crypto_price(query))
            await message.reply("\n\n".join(replies))
            return
            
    if has_news:
        await message.reply(get_crypto_news())
        return

    # Handle AI Chat
    if is_directed_at_bot:
        reply = ai_reply(message)
        await message.reply(reply)

# -------- Start the bot -------- #

client.run(TOKEN)
