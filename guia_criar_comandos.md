# 📖 Guia Completo: Criando Comandos para Seu 🤖🎶 Bot de Música no Discord

## 🚀 Introdução

Você já tem um bot de música rodando no Discord e está pronto para dar o próximo passo: criar novos comandos que vão tornar o bot mais poderoso e útil para você e seus amigos. Neste guia, vou ensinar como criar comandos variados, desde os mais simples até os mais sofisticados, com base no seu bot em Python.

Teremos várias seções, onde aprenderemos a:

- 📜 Entender o código existente e os conceitos por trás dele.
- 🛠️ Criar novos comandos básicos como `mute`, `volume` e `resume`.
- 🔄 Implementar comandos complexos como `queue` para uma fila de músicas.
- 🤖 Automatizar algumas funcionalidades do bot e torná-lo ainda mais interativo.
- 🎵 Tocar músicas de outras plataformas, como Spotify e Deezer.
- ✨ Criar comandos personalizados e aprimorar a experiência musical.
- 🌐 Explorar funcionalidades avançadas e integrar com serviços populares.

## Parte 1: Compreendendo o Código 📝

O arquivo `bot.py` atual contém os seguintes comandos:

- `play`: Para tocar músicas do YouTube.
- `join` e `leave`: Fazem o bot entrar ou sair de um canal de voz.
- `stop`: Interrompe a música que está tocando.
- `ping`: Mostra a latência do bot.

Agora, vamos expandir as funcionalidades do bot, criando novos comandos que complementam os existentes e adicionam novos recursos.

### Estrutura do Comando do Bot 🛠️

Os comandos são criados usando o decorador `@client.command()`, que é fornecido pela extensão `commands` da biblioteca `discord.py`. Cada comando é uma função Python que responde a um comando digitado pelo usuário no chat do Discord. Isso significa que você tem controle total sobre o que o bot faz quando recebe um comando.

Vamos relembrar a sintaxe de criação de um comando:

```python
@client.command(name='nome_do_comando')
async def nome_do_comando(ctx, *args):
    # Código do comando aqui
```

- `ctx` é o contexto do comando, que dá acesso a informações como o canal e o autor.
- `*args` são argumentos adicionais que o usuário pode fornecer.

## Parte 2: Criando Comandos Básicos 🔧

### 1. Comando `mute`

Vamos criar um comando que permite ao usuário silenciar o bot enquanto ele estiver tocando música.

```python
@client.command(name='mute')
async def mute(ctx):
    if ctx.voice_client is None:
        await ctx.send('❌ O bot não está em um canal de voz.')
        return
    ctx.voice_client.source.volume = 0.0
    await ctx.send('🔇 Bot mutado.')
```

Esse comando define o volume da fonte de áudio do bot como `0.0`, silenciando a música.

### 2. Comando `resume`

Para retomar a música após ter parado ou pausado, vamos criar um comando `resume`.

```python
@client.command(name='resume')
async def resume(ctx):
    if ctx.voice_client is None:
        await ctx.send('❌ O bot não está em um canal de voz.')
        return
    if ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send('▶️ Música retomada.')
    else:
        await ctx.send('Nenhuma música está pausada.')
```

Esse comando verifica se a música está pausada e, se estiver, retoma a reprodução.

### 3. Comando `volume`

Você também pode criar um comando para definir o volume do bot. Esse comando permite que o usuário especifique o volume desejado entre 0 e 100.

```python
@client.command(name='volume')
async def volume(ctx, volume: int):
    if ctx.voice_client is None:
        await ctx.send('❌ O bot não está em um canal de voz.')
        return
    if 0 <= volume <= 100:
        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f'🔊 Volume definido para {volume}%.')
    else:
        await ctx.send('Por favor, forneça um valor entre 0 e 100.')
```

## Parte 3: Comandos Avançados 🚀

### 1. Comando `queue` para Fila de Músicas

Um recurso essencial em bots de música é a capacidade de criar uma fila de músicas, onde várias faixas podem ser adicionadas e tocadas em sequência. Vamos adicionar esse recurso ao nosso bot.

**Definindo a variável `queue`:**

Primeiro, precisamos definir uma lista para armazenar a fila de músicas. Coloque essa definição no início do seu código, fora de qualquer função:

```python
queue = []
```

**Comando `queue` para adicionar músicas à fila:**

```python
@client.command(name='queue')
async def queue_music(ctx, *, url: str):
    global queue
    queue.append(url)
    await ctx.send(f'🎵 Música adicionada à fila: {url}')
```

**Modificando o comando `play` para tocar as músicas da fila:**

```python
@client.command(name='play')
async def play(ctx, *, url: str = None):
    global queue
    if ctx.voice_client is None:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send('❌ Você não está conectado a um canal de voz.')
            return

    if url:
        queue.append(url)
        await ctx.send(f'🎵 Música adicionada à fila: {url}')

    if not ctx.voice_client.is_playing() and queue:
        await play_next(ctx)
```

**Função `play_next` para tocar a próxima música:**

```python
async def play_next(ctx):
    global queue
    if queue:
        url = queue.pop(0)
        player = await YTDLSource.from_url(url, loop=client.loop, stream=True)
        if player is None:
            await ctx.send('❌ Erro ao obter a música.')
            await play_next(ctx)
            return

        def after_playing(error):
            fut = asyncio.run_coroutine_threadsafe(play_next(ctx), client.loop)
            try:
                fut.result()
            except Exception as e:
                print(f'Erro ao tocar a próxima música: {e}')

        ctx.voice_client.play(player, after=after_playing)
        await ctx.send(f'🎶 Tocando agora: {player.title}')
    else:
        await ctx.send('A fila terminou.')
```

**Nota Importante:**

Certifique-se de que a variável `queue` está definida no escopo global. Se você receber o erro `NameError: name 'queue' is not defined`, significa que o Python não reconhece a variável `queue` dentro da função. Para corrigir isso, declare a variável `queue` como global dentro das funções que a modificam:

```python
global queue
```

Por exemplo:

```python
@client.command(name='queue')
async def queue_music(ctx, *, url: str):
    global queue
    queue.append(url)
    await ctx.send(f'🎵 Música adicionada à fila: {url}')
```

Faça isso em todas as funções onde você modifica a variável `queue`.

### 2. Comando `skip`

Para pular para a próxima música da fila, vamos criar o comando `skip`.

```python
@client.command(name='skip')
async def skip(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send('⏭️ Música pulada.')
    else:
        await ctx.send('Nenhuma música está tocando no momento.')
```

Esse comando interrompe a música atual e automaticamente aciona a função `play_next` para tocar a próxima música na fila.

### 3. Comando `pause`

Podemos também adicionar um comando para pausar a música.

```python
@client.command(name='pause')
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send('⏸️ Música pausada.')
    else:
        await ctx.send('Nenhuma música está tocando no momento.')
```

### 4. Comando `clear_queue`

Se você quiser limpar todas as músicas da fila, pode criar um comando `clear_queue`.

```python
@client.command(name='clear_queue')
async def clear_queue(ctx):
    global queue
    queue.clear()
    await ctx.send('🗑️ A fila de músicas foi limpa.')
```

## Parte 4: Melhorias e Automação 🤖

### 1. Mensagem de Boas-Vindas

Vamos adicionar um comando que envie uma mensagem de boas-vindas sempre que o bot entrar em um servidor.

```python
@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send('👋 Olá! Eu sou um bot de música. Use `$$help` para ver meus comandos!')
            break
```

### 2. Reação a Mensagens Específicas

Podemos fazer o bot reagir a palavras-chave nas mensagens.

```python
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if 'música' in message.content.lower():
        await message.channel.send('🎵 Você quer tocar uma música? Use `$$play <nome>`!')

    await client.process_commands(message)
```

## Parte 5: Criando Funções Personalizadas ✨

### 1. Comando `shuffle`

Vamos criar um comando `shuffle` para embaralhar as músicas na fila.

```python
import random

@client.command(name='shuffle')
async def shuffle(ctx):
    global queue
    if len(queue) > 1:
        random.shuffle(queue)
        await ctx.send('🔀 A fila foi embaralhada!')
    else:
        await ctx.send('A fila está vazia ou tem apenas uma música.')
```

### 2. Comando `now_playing`

Podemos adicionar um comando para mostrar qual música está tocando no momento.

```python
@client.command(name='now_playing')
async def now_playing(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        await ctx.send(f'🎵 Tocando agora: {ctx.voice_client.source.title}')
    else:
        await ctx.send('Nenhuma música está tocando no momento.')
```

## Parte 6: Melhorando a Experiência do Usuário 😊

### 1. Adicionando Emojis

Adicionar emojis nas respostas do bot pode tornar a experiência mais divertida. Já fizemos isso em alguns comandos.

### 2. Adicionando Feedback de Erro

Vamos adicionar mensagens de erro personalizadas para tornar o uso do bot mais claro.

```python
@client.command(name='join')
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await channel.connect()
            await ctx.send('✅ Conectado ao canal de voz!')
        else:
            await ctx.voice_client.move_to(channel)
            await ctx.send('✅ Movido para o seu canal de voz!')
    else:
        await ctx.send('❌ Você não está conectado a um canal de voz.')
```

## Parte 7: Tocar Músicas de Outras Plataformas (Spotify, Deezer, etc.)

### 1. Integração com Spotify

Para tocar músicas do Spotify, vamos usar a biblioteca `spotipy`.

**Instalação:**

```bash
pip install spotipy
```

**Configuração:**

Crie um aplicativo no [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) e obtenha seu `client_id` e `client_secret`.

No seu arquivo `.env`, adicione:

```env
SPOTIFY_CLIENT_ID='seu_client_id'
SPOTIFY_CLIENT_SECRET='seu_client_secret'
```

**Código:**

```python
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv('SPOTIFY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')
))
```

**Comando `play_spotify`:**

```python
@client.command(name='play_spotify')
async def play_spotify(ctx, *, track_name: str):
    results = sp.search(q=track_name, type='track', limit=1)
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        song_name = f"{track['name']} {track['artists'][0]['name']}"
        query = f"ytsearch:{song_name}"
        global queue
        queue.append(query)
        await ctx.send(f'🎵 Música adicionada à fila: {song_name}')
        if not ctx.voice_client.is_playing():
            await play_next(ctx)
    else:
        await ctx.send('Nenhuma música foi encontrada no Spotify.')
```

**Nota:**

Como o Discord não permite reproduzir diretamente do Spotify, buscamos a música no YouTube com base no nome da faixa e do artista.

### 2. Integração com Deezer

Para integrar com o Deezer, podemos usar a API pública do Deezer.

**Instalação:**

```bash
pip install requests
```

**Comando `play_deezer`:**

```python
import requests

@client.command(name='play_deezer')
async def play_deezer(ctx, *, track_name: str):
    url = f'https://api.deezer.com/search?q={track_name}'
    response = requests.get(url)
    data = response.json()
    if data['data']:
        track = data['data'][0]
        song_name = f"{track['title']} {track['artist']['name']}"
        query = f"ytsearch:{song_name}"
        global queue
        queue.append(query)
        await ctx.send(f'🎵 Música adicionada à fila: {song_name}')
        if not ctx.voice_client.is_playing():
            await play_next(ctx)
    else:
        await ctx.send('Nenhuma música foi encontrada no Deezer.')
```

## Parte 8: Criando Seus Próprios Comandos Personalizados 🛠️

### 1. Comando `lyrics` para Mostrar Letras de Músicas

Para buscar as letras das músicas, podemos usar a API do Genius.

**Instalação:**

```bash
pip install lyricsgenius
```

**Configuração:**

Crie um aplicativo no [Genius API](https://genius.com/developers) e obtenha sua `GENIUS_API_KEY`. Adicione no seu arquivo `.env`:

```env
GENIUS_API_KEY='sua_genius_api_key'
```

**Código:**

```python
import lyricsgenius

genius = lyricsgenius.Genius(os.getenv('GENIUS_API_KEY'))
```

**Comando `lyrics`:**

```python
@client.command(name='lyrics')
async def lyrics(ctx, *, track_name: str):
    song = genius.search_song(track_name)
    if song:
        lyrics_text = song.lyrics
        for chunk in [lyrics_text[i:i+2000] for i in range(0, len(lyrics_text), 2000)]:
            await ctx.send(chunk)
    else:
        await ctx.send('Não foi possível encontrar a letra da música.')
```

### 2. Comando `recommend` para Recomendação de Músicas

Vamos criar um comando que sugere músicas com base na música que está sendo tocada.

```python
@client.command(name='recommend')
async def recommend(ctx, *, track_name: str):
    results = sp.search(q=track_name, type='track', limit=1)
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        recommendations = sp.recommendations(seed_tracks=[track['id']], limit=5)
        recommendation_list = '\n'.join([f"{idx + 1}. {rec['name']} - {rec['artists'][0]['name']}" for idx, rec in enumerate(recommendations['tracks'])])
        await ctx.send(f'Recomendações com base em "{track_name}":\n{recommendation_list}')
    else:
        await ctx.send('Nenhuma recomendação foi encontrada.')
```

## 🎉 Conclusão

Este guia mostrou como você pode adicionar funcionalidades incríveis ao seu bot de música no Discord. Agora seu bot pode:

- Mudar volume, silenciar, pausar e retomar músicas.
- Gerenciar uma fila de músicas com comandos como `queue`, `skip`, `clear_queue`, `shuffle` e `now_playing`.
- Integrar com plataformas populares como Spotify e Deezer.
- Buscar letras de músicas e fornecer recomendações musicais.
- Melhorar a interação com os usuários por meio de mensagens de boas-vindas, emojis e respostas personalizadas.

Você pode continuar expandindo o bot adicionando mais comandos e funcionalidades que fizerem sentido para o seu uso. Divirta-se programando e aprimorando seu bot! Caso precise de mais ideias ou ajuda, estou à disposição para colaborar mais.

---

**Código Completo Ajustado:**

Aqui está o código completo do bot com todas as correções, incluindo a definição da variável `queue` e a declaração `global queue` nas funções que a modificam.

```python
import os
import discord
from discord.ext import commands
import youtube_dl
import asyncio
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import requests
import lyricsgenius

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

# Configurações do YouTube DL
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': False,
    'ignoreerrors': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
}

ffmpeg_options = {
    'options': '-vn'
}

# Instância do YouTube DL
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

# Classe para reproduzir áudio
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if data is None:
            return None

        if 'entries' in data:
            data = data['entries'][0]

        if data is None:
            return None

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

# Inicializa o bot
intents = discord.Intents.all()
client = commands.Bot(command_prefix='$$', intents=intents)

# Variável global para a fila de músicas
queue = []

# Configuração do Spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv('SPOTIFY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')
))

# Configuração do Genius API para letras de músicas
genius = lyricsgenius.Genius(os.getenv('GENIUS_API_KEY'))

# Comando play
@client.command(name='play')
async def play(ctx, *, url: str = None):
    global queue
    if ctx.voice_client is None:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send('❌ Você não está conectado a um canal de voz.')
            return

    if url:
        queue.append(url)
        await ctx.send(f'🎵 Música adicionada à fila: {url}')

    if not ctx.voice_client.is_playing() and queue:
        await play_next(ctx)

async def play_next(ctx):
    global queue
    if queue:
        url = queue.pop(0)
        player = await YTDLSource.from_url(url, loop=client.loop, stream=True)
        if player is None:
            await ctx.send('❌ Erro ao obter a música.')
            await play_next(ctx)
            return

        def after_playing(error):
            fut = asyncio.run_coroutine_threadsafe(play_next(ctx), client.loop)
            try:
                fut.result()
            except Exception as e:
                print(f'Erro ao tocar a próxima música: {e}')

        ctx.voice_client.play(player, after=after_playing)
        await ctx.send(f'🎶 Tocando agora: {player.title}')
    else:
        await ctx.send('A fila terminou.')

# Comando queue
@client.command(name='queue')
async def queue_music(ctx, *, url: str):
    global queue
    queue.append(url)
    await ctx.send(f'🎵 Música adicionada à fila: {url}')

# Comando skip
@client.command(name='skip')
async def skip(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send('⏭️ Música pulada.')
    else:
        await ctx.send('Nenhuma música está tocando no momento.')

# Comando pause
@client.command(name='pause')
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send('⏸️ Música pausada.')
    else:
        await ctx.send('Nenhuma música está tocando no momento.')

# Comando resume
@client.command(name='resume')
async def resume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send('▶️ Música retomada.')
    else:
        await ctx.send('Nenhuma música está pausada.')

# Comando mute
@client.command(name='mute')
async def mute(ctx):
    if ctx.voice_client and ctx.voice_client.source:
        ctx.voice_client.source.volume = 0.0
        await ctx.send('🔇 Bot mutado.')
    else:
        await ctx.send('❌ Não há música sendo reproduzida.')

# Comando volume
@client.command(name='volume')
async def volume(ctx, volume: int):
    if ctx.voice_client and ctx.voice_client.source:
        if 0 <= volume <= 100:
            ctx.voice_client.source.volume = volume / 100
            await ctx.send(f'🔊 Volume definido para {volume}%.')
        else:
            await ctx.send('Por favor, forneça um valor entre 0 e 100.')
    else:
        await ctx.send('❌ Não há música sendo reproduzida.')

# Comando shuffle
@client.command(name='shuffle')
async def shuffle_queue(ctx):
    global queue
    if len(queue) > 1:
        random.shuffle(queue)
        await ctx.send('🔀 A fila foi embaralhada!')
    else:
        await ctx.send('A fila está vazia ou tem apenas uma música.')

# Comando clear_queue
@client.command(name='clear_queue')
async def clear_queue(ctx):
    global queue
    queue.clear()
    await ctx.send('🗑️ A fila de músicas foi limpa.')

# Comando now_playing
@client.command(name='now_playing')
async def now_playing(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        await ctx.send(f'🎵 Tocando agora: {ctx.voice_client.source.title}')
    else:
        await ctx.send('Nenhuma música está tocando no momento.')

# Comando join
@client.command(name='join')
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await channel.connect()
            await ctx.send('✅ Conectado ao canal de voz!')
        else:
            await ctx.voice_client.move_to(channel)
            await ctx.send('✅ Movido para o seu canal de voz!')
    else:
        await ctx.send('❌ Você não está conectado a um canal de voz.')

# Comando leave
@client.command(name='leave')
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send('📴 Desconectado do canal de voz.')
    else:
        await ctx.send('❌ O bot não está em um canal de voz.')

# Evento on_guild_join
@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send('👋 Olá! Eu sou um bot de música. Use `$$help` para ver meus comandos!')
            break

# Evento on_message
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if 'música' in message.content.lower():
        await message.channel.send('🎵 Você quer tocar uma música? Use `$$play <nome>`!')

    await client.process_commands(message)

# Comando play_spotify
@client.command(name='play_spotify')
async def play_spotify(ctx, *, track_name: str):
    global queue
    results = sp.search(q=track_name, type='track', limit=1)
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        song_name = f"{track['name']} {track['artists'][0]['name']}"
        query = f"ytsearch:{song_name}"
        queue.append(query)
        await ctx.send(f'🎵 Música adicionada à fila: {song_name}')
        if not ctx.voice_client.is_playing():
            await play_next(ctx)
    else:
        await ctx.send('Nenhuma música foi encontrada no Spotify.')

# Comando lyrics
@client.command(name='lyrics')
async def lyrics(ctx, *, track_name: str):
    song = genius.search_song(track_name)
    if song:
        lyrics_text = song.lyrics
        for chunk in [lyrics_text[i:i+2000] for i in range(0, len(lyrics_text), 2000)]:
            await ctx.send(chunk)
    else:
        await ctx.send('Não foi possível encontrar a letra da música.')

# Comando recommend
@client.command(name='recommend')
async def recommend(ctx, *, track_name: str):
    results = sp.search(q=track_name, type='track', limit=1)
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        recommendations = sp.recommendations(seed_tracks=[track['id']], limit=5)
        recommendation_list = '\n'.join([f"{idx + 1}. {rec['name']} - {rec['artists'][0]['name']}" for idx, rec in enumerate(recommendations['tracks'])])
        await ctx.send(f'Recomendações com base em "{track_name}":\n{recommendation_list}')
    else:
        await ctx.send('Nenhuma recomendação foi encontrada.')

# Comando ping
@client.command(name='ping')
async def ping(ctx):
    await ctx.send(f'🏓 Pong! Latência: {round(client.latency * 1000)}ms')

# Inicia o bot
client.run(TOKEN)
```

**Observações Importantes:**

- **Definição da Variável `queue`:**

  A variável `queue` deve ser definida no escopo global, fora de qualquer função.

- **Uso de `global queue`:**

  Dentro de cada função que modifica `queue`, inclua a declaração `global queue` para garantir que você está modificando a variável global e não criando uma nova variável local.

- **Verificações Adicionais:**

  Incluí verificações para lidar com possíveis erros, como falha ao obter informações da música. Isso ajuda a evitar que o bot pare de funcionar inesperadamente.

- **Instalação de Bibliotecas:**

  Certifique-se de instalar todas as bibliotecas necessárias com o comando:

  ```bash
  pip install discord.py youtube_dl spotipy python-dotenv requests lyricsgenius
  ```

- **Configuração das Credenciais:**

  Crie um arquivo `.env` na mesma pasta do seu script e adicione as seguintes linhas, substituindo pelos seus dados:

  ```env
  DISCORD_TOKEN='seu_token_do_bot'
  SPOTIFY_CLIENT_ID='seu_spotify_client_id'
  SPOTIFY_CLIENT_SECRET='seu_spotify_client_secret'
  GENIUS_API_KEY='sua_genius_api_key'
  ```

- **Permissões do Bot:**

  Assegure-se de que o bot tem as permissões adequadas no seu servidor Discord para enviar mensagens e conectar-se aos canais de voz.

- **Atualizações Futuras:**

  Mantenha as bibliotecas atualizadas e fique atento às mudanças nas APIs que você está utilizando para evitar que o bot pare de funcionar devido a atualizações ou alterações nas plataformas.
