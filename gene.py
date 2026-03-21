import discord
from discord import app_commands
import requests
import os
import re
import asyncio
import wavelink
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_KEY = os.getenv("GROQ_API_KEY")

intents = discord.Intents.default()
intents.message_content = True

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        # Use a stable public Lavalink node. 
        # Public nodes are great for testing and quick setups without hosting Java ourselves.
        nodes = [
            wavelink.Node(
                uri="https://lavalink.lexis.host:443", 
                password="lexishostlavalink",
                inactive_timeout=180
            )
        ]
        try:
            await wavelink.Pool.connect(nodes=nodes, client=self)
            print("[WAVELINK] Successfully connected to Lavalink node.", flush=True)
        except Exception as e:
            print(f"[WAVELINK] Connection failed: {e}", flush=True)

client = MyClient(intents=intents)
tree = client.tree

# -------- Music Events -------- #

@client.event
async def on_wavelink_node_ready(payload: wavelink.NodeReadyEventPayload):
    print(f"[WAVELINK] Node {payload.node.identifier} is ready!", flush=True)

# -------- Slash Commands for Music -------- #

@tree.command(name="play", description="Play a song (YouTube/SoundCloud search)")
async def play(interaction: discord.Interaction, query: str):
    if not interaction.guild:
        await interaction.response.send_message("❌ This command must be used in a server!")
        return

    if not interaction.user.voice:
        await interaction.response.send_message("❌ You need to join a voice channel first!")
        return

    await interaction.response.defer()

    try:
        # Search for tracks using the Lavalink node's technology
        # This handles filtering and avoids local IP blocks!
        tracks: wavelink.Search = await wavelink.Playable.search(query)
        if not tracks:
            await interaction.followup.send(f"❌ Could not find search results for: `{query}`")
            return

        track = tracks[0]

        # Join or move to the user's voice channel
        vc: wavelink.Player = interaction.guild.voice_client 

        if not vc:
            vc = await interaction.user.voice.channel.connect(cls=wavelink.Player)
        elif vc.channel != interaction.user.voice.channel:
            await vc.move_to(interaction.user.voice.channel)

        if vc.playing:
            vc.queue.put(track)
            await interaction.followup.send(f"➕ Added to queue: **{track.title}**")
        else:
            await vc.play(track)
            await interaction.followup.send(f"🎶 Now playing: **{track.title}**")

    except Exception as e:
        print(f"Play Error: {e}", flush=True)
        await interaction.followup.send(f"❌ An error occurred while trying to play: `{str(e)}`")

@tree.command(name="skip", description="Skip the current song")
async def skip(interaction: discord.Interaction):
    vc: wavelink.Player = interaction.guild.voice_client
    if not vc or not vc.playing:
        return await interaction.response.send_message("❌ Nothing is currently playing.")
    
    await vc.skip()
    await interaction.response.send_message("⏭️ Skipped the current song!")

@tree.command(name="stop", description="Stop the music and leave the channel")
async def stop(interaction: discord.Interaction):
    vc: wavelink.Player = interaction.guild.voice_client
    if vc:
        await vc.disconnect()
        await interaction.response.send_message("⏹️ Stopped the music and left the voice channel.")
    else:
        await interaction.response.send_message("❌ I'm not in a voice channel.")

# -------- Crypto APIs (CoinGecko) -------- #

def get_crypto_price(query):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(f"https://api.coingecko.com/api/v3/search?query={query}", headers=headers).json()
        if r.get("coins"):
            coin_id = r["coins"][0]["id"]
            p = requests.get(f"https://api.coingecko.com/api/v3/coins/{coin_id}?localization=false&tickers=false&market_data=true", headers=headers).json()
            if "market_data" in p:
                md = p["market_data"]
                usd_price = md.get("current_price", {}).get("usd", "N/A")
                change = md.get("price_change_percentage_24h", "N/A")
                return f"**{p['name']} ({p['symbol'].upper()})**\n💰 **Price:** ${usd_price} USD\n📅 **24h Change:** {change}%"
    except: pass
    return f"I couldn't find any crypto data for `{query}`!"

# -------- AI Chat using Groq -------- #

def ai_reply(message):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    
    user_context = f"{message.author.display_name} says: {message.content}"
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "You are Homeless Girl, a playful, flirty girl chatting in Discord. Speak casually and use sweet words like baby, darling, sweetheart, and handsome. Keep replies short and cute."},
            {"role": "user", "content": user_context}
        ],
        "temperature": 1,
        "max_tokens": 100
    }
    try:
        r = requests.post(url, headers=headers, json=data)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
    except: pass
    return "Oops! I'm having a little brain freeze, baby. 🥺"

# -------- Main Events -------- #

@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user}", flush=True)

@client.event
async def on_message(message):
    if message.author == client.user: return
    text = message.content.lower()
    
    # Check for $token price requests
    if "$" in text:
        token_match = re.search(r'\$([a-zA-Z]+)', text)
        if token_match:
            await message.reply(get_crypto_price(token_match.group(1)))
            return

    # Check for AI Chat triggers
    if "homeless girl" in text or client.user in message.mentions:
        reply = ai_reply(message)
        await message.reply(reply)

# -------- Launch the Bot -------- #
client.run(TOKEN)
