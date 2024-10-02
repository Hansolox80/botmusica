import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import asyncio

# Substitua 'YOUR_BOT_TOKEN' pelo token do seu bot
TOKEN = 'YOUR_BOT_TOKEN'

# Intents são necessários para acessar certos eventos
intents = discord.Intents.default()
intents.message_content = True

# Prefixo para os comandos do bot
client = commands.Bot(command_prefix='$$', intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} online!')

# Configurações do yt_dlp
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
    'source_address': '0.0.0.0'  # ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

@client.command(name='play')
async def play(ctx, *, search: str):
    async with ctx.typing():
        # Executa a busca de músicas no YouTube
        info = await asyncio.get_event_loop().run_in_executor(None, lambda: ytdl.extract_info(f"ytsearch5:{search}", download=False))

        if not info or 'entries' not in info:
            await ctx.send('Nenhum resultado encontrado.')
            return

        entries = info['entries']
        result_message = '\n'.join([f"{i+1}. {entry['title']}" for i, entry in enumerate(entries)])
        await ctx.send(f"Selecione uma música:\n{result_message}")

        def check(m):
            return m.author == ctx.author and m.content.isdigit() and 1 <= int(m.content) <= 5

        try:
            response = await client.wait_for('message', check=check, timeout=30.0)
        except asyncio.TimeoutError:
            await ctx.send('Tempo esgotado para selecionar uma música.')
            return

        selection = int(response.content) - 1
        url = entries[selection]['webpage_url']
        player = await YTDLSource.from_url(url, loop=client.loop, stream=True)
        ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Agora tocando: {player.title}')

@client.command(name='join')
async def join(ctx):
    if not ctx.author.voice:
        await ctx.send("Você não está conectado a um canal de voz.")
        return
    channel = ctx.author.voice.channel
    await channel.connect()

@client.command(name='leave')
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()

@client.command(name='stop')
async def stop(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()

@client.command(name='ping')
async def ping(ctx):
    bot_latency = round(client.latency * 1000)  # Latência do bot em milissegundos
    message = await ctx.send("Calculando latência...")

    # Latência da API baseada na diferença de tempo entre a mensagem original e a resposta
    api_latency = (message.created_at - ctx.message.created_at).total_seconds() * 1000

    embed = discord.Embed(
        title="🏓 Pong!",
        description="Aqui estão as latências:",
        color=discord.Color.blue()  # Você pode escolher outra cor se quiser
    )
    
    embed.add_field(name="Bot Latency", value=f"`{bot_latency}ms`", inline=False)
    embed.add_field(name="API Latency", value=f"`{round(api_latency)}ms`", inline=False)

    await message.edit(content=None, embed=embed)

# Inicia o bot
client.run(TOKEN)
