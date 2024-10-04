# 📖 Guia Completo: Criando Comandos para Seu 🤖🎶 Bot de Música no Discord

## 🚀 Introdução

Você já tem um 🤖 bot de 🎶 música rodando no Discord e está pronto para dar o próximo passo: criar novos comandos que vão tornar o bot mais poderoso 💪 e útil 🔧 para você e seus amigos 👥. Neste guia, vou ensinar como criar comandos variados, desde os mais simples até os mais sofisticados, com base no seu bot em 🐍 Python.

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

- `▶️ play`: Para tocar músicas do 🎥 YouTube.
- `📥 join` e `📤 leave`: Fazem o bot entrar ou sair de um canal de voz 🎤.
- `⏹️ stop`: Interrompe a 🎶 música que está tocando.
- `🏓 ping`: Mostra a 📊 latência do bot.

Agora, vamos expandir as funcionalidades do bot, criando novos comandos que complementam os existentes e adicionam novos recursos ✨.

### Estrutura do Comando do Bot 🛠️

Os comandos são criados usando o decorador `@client.command()`, que é fornecido pela extensão `commands` da biblioteca `discord.py`. Cada comando é uma função 🐍 Python que responde a um comando digitado pelo usuário no chat do Discord. Isso significa que você tem controle total sobre o que o bot faz quando recebe um comando.

Vamos relembrar a sintaxe de criação de um comando:

```python
@client.command(name='nome_do_comando')
async def nome_do_comando(ctx, *args):
    # Código do comando aqui 💻
```

- `ctx` é o contexto do comando, que dá acesso a informações como o canal 📺 e o autor ✍️.
- `*args` são argumentos adicionais que o usuário pode fornecer.

## Parte 2: Criando Comandos Básicos 🔧

### 1. Comando `🔇 mute`

Vamos criar um comando que permite ao usuário silenciar 🔇 o bot enquanto ele estiver tocando 🎶 música.

```python
@client.command(name='mute')
async def mute(ctx):
    if ctx.voice_client is None:
        await ctx.send('❌ O bot não está em um canal de voz.')
        return
    ctx.voice_client.source.volume = 0.0
    await ctx.send('🔇 Bot mutado.')
```

Esse comando define o 🔊 volume da fonte de áudio do bot como `0.0`, silenciando 🔕 a música.

### 2. Comando `⏯️ resume`

Para retomar a 🎶 música após ter parado ⏹️ ou pausado ⏸️, vamos criar um comando `resume`.

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
        await ctx.send('Nenhuma 🎶 música está pausada.')
```

Esse comando verifica se a música está pausada e, se estiver, retoma a reprodução ▶️.

### 3. Comando `🔊 volume`

Você também pode criar um comando para definir o volume 🔊 do bot. Esse comando permite que o usuário especifique o volume desejado entre 0 e 100.

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

### 1. Comando `📜 queue` para Fila de Músicas 🎶

Um recurso essencial em bots de 🎶 música é a capacidade de criar uma fila 📜 de músicas, onde várias faixas podem ser adicionadas e tocadas em sequência 🔄. Vamos adicionar esse recurso ao nosso bot.

Vamos precisar de uma lista 📋 para armazenar os links das músicas e algumas funções para manipular essa lista.

Primeiro, definimos uma lista para a fila:

```python
queue = []
```

Depois, podemos criar um comando `queue` para adicionar músicas à fila:

```python
@client.command(name='queue')
async def queue_music(ctx, *, url: str):
    queue.append(url)
    await ctx.send(f'🎵 Música adicionada à fila: {url}')
```

Agora, vamos modificar o comando `play` para tocar as músicas da fila:

```python
@client.command(name='play')
async def play(ctx, *, url: str = None):
    if ctx.voice_client is None:
        await ctx.author.voice.channel.connect()
    
    if url:
        queue.append(url)
    
    if not ctx.voice_client.is_playing() and queue:
        player = await YTDLSource.from_url(queue.pop(0), loop=client.loop, stream=True)
        ctx.voice_client.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), client.loop))
        await ctx.send(f'🎶 Tocando agora: {player.title}')
```

E uma função para tocar a próxima música automaticamente 🔄:

```python
async def play_next(ctx):
    if queue:
        player = await YTDLSource.from_url(queue.pop(0), loop=client.loop, stream=True)
        ctx.voice_client.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), client.loop))
        await ctx.send(f'🎶 Tocando agora: {player.title}')
```

### 2. Comando `⏭️ skip`

Para pular para a próxima música da fila, vamos criar o comando `skip`.

```python
@client.command(name='skip')
async def skip(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send('⏭️ Música pulada.')
    else:
        await ctx.send('Nenhuma 🎶 música está tocando no momento.')
```

Esse comando interrompe a 🎶 música atual e automaticamente aciona a função `play_next` para tocar a próxima música na fila.

### 3. Comando `⏸️ pause`

Podemos também adicionar um comando para pausar a música.

```python
@client.command(name='pause')
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send('⏸️ Música pausada.')
    else:
        await ctx.send('Nenhuma 🎶 música está tocando no momento.')
```

### 4. Comando `🗑️ clear_queue`

Se você quiser limpar todas as músicas da fila, pode criar um comando `clear_queue`.

```python
@client.command(name='clear_queue')
async def clear_queue(ctx):
    queue.clear()
    await ctx.send('🗑️ A fila de músicas foi limpa.')
```

## Parte 4: Melhorias e Automação 🤖

### 1. Mensagem de Boas-Vindas 👋

Vamos adicionar um comando que envie uma mensagem de boas-vindas sempre que o bot entrar em um servidor.

```python
@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send('👋 Olá! Eu sou um bot de 🎶 música. Use `$$help` para ver meus comandos!')
            break
```

### 2. Reação a Mensagens Específicas 💬

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

### 1. Comando `🔀 shuffle`

Vamos criar um comando `shuffle` para embaralhar as músicas na fila.

```python
import random

@client.command(name='shuffle')
async def shuffle(ctx):
    if len(queue) > 1:
        random.shuffle(queue)
        await ctx.send('🔀 A fila foi embaralhada!')
    else:
        await ctx.send('A fila está vazia ou tem apenas uma música.')
```

Esse comando usa a função `random.shuffle()` para reorganizar as músicas na fila.

### 2. Comando `🎵 now_playing`

Podemos adicionar um comando para mostrar qual música está tocando no momento.

```python
@client.command(name='now_playing')
async def now_playing(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        await ctx.send(f'🎵 Tocando agora: {ctx.voice_client.source.title}')
    else:
        await ctx.send('Nenhuma 🎶 música está tocando no momento.')
```

## Parte 6: Melhorando a Experiência do Usuário 😊

### 1. Adicionando Emojis 😃

Adicionar emojis nas respostas do bot pode tornar a experiência mais divertida. Vamos modificar o comando `play` para incluir emojis.

```python
@client.command(name='play')
async def play(ctx, *, url: str = None):
    if ctx.voice_client is None:
        await ctx.author.voice.channel.connect()
    
    if url:
        queue.append(url)
    
    if not ctx.voice_client.is_playing() and queue:
        player = await YTDLSource.from_url(queue.pop(0), loop=client.loop, stream=True)
        ctx.voice_client.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), client.loop))
        await ctx.send(f'🎶 Tocando agora: {player.title}')
```

### 2. Adicionando Feedback de Erro ⚠️

Vamos adicionar mensagens de erro personalizadas para tornar o uso do bot mais claro.

```python
@client.command(name='join')
async def join(ctx):
    if not ctx.author.voice:
        await ctx.send('❌ Você não está conectado a um canal de voz.')
        return
    channel = ctx.author.voice.channel
    await channel.connect()
    await ctx.send('✅ Conectado ao canal de voz!')
```

## Parte 7: Tocar Músicas de Outras Plataformas (Spotify, Deezer, etc.) 🎶🌐

### 1. Integração com Spotify e Deezer 🎵

Para tocar músicas do Spotify ou Deezer, é necessário utilizar uma biblioteca que suporte a extração dos links dessas plataformas e os converta em um formato compatível com o Discord. Neste exemplo, vamos usar a API do Spotify para buscar músicas e tocá-las no bot.

Primeiro, instale a biblioteca `spotipy`:

```bash
pip install spotipy
```

Você precisará criar um aplicativo no [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) para obter as credenciais necessárias. Crie um arquivo `.env` para armazenar as credenciais do Spotify:

```env
SPOTIFY_CLIENT_ID='seu_client_id'
SPOTIFY_CLIENT_SECRET='seu_client_secret'
SPOTIFY_REDIRECT_URI='sua_redirect_uri'
```

Agora, vamos configurar a autenticação do Spotify no código do bot:

```python
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv('SPOTIFY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')
))
```

Vamos criar um comando `play_spotify` para tocar músicas do Spotify:

```python
@client.command(name='play_spotify')
async def play_spotify(ctx, *, track_name: str):
    results = sp.search(q=track_name, type='track', limit=1)
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        url = track['external_urls']['spotify']
        await ctx.send(f'🔊 Tocando agora no Spotify: {track["name"]} - {track["artists"][0]["name"]}\n{url}')
    else:
        await ctx.send('Nenhuma 🎶 música foi encontrada no Spotify.')
```

### 2. Integração com Deezer 🎶

Para integrar com Deezer, você pode usar a API do Deezer e realizar buscas por músicas de forma semelhante. Assim como fizemos com o Spotify, será necessário configurar as credenciais e realizar buscas através da API do Deezer.

Instale a biblioteca `requests` para realizar as requisições à API do Deezer:

```bash
pip install requests
```

Agora, vamos criar um comando `play_deezer` para tocar músicas do Deezer:

```python
import requests

@client.command(name='play_deezer')
async def play_deezer(ctx, *, track_name: str):
    url = f'https://api.deezer.com/search?q={track_name}'
    response = requests.get(url)
    data = response.json()
    if data['data']:
        track = data['data'][0]
        await ctx.send(f'🔊 Tocando agora no Deezer: {track["title"]} - {track["artist"]["name"]}\n{track["link"]}')
    else:
        await ctx.send('Nenhuma 🎶 música foi encontrada no Deezer.')
```

## Parte 8: Criando Seus Próprios Comandos Personalizados 🛠️

Agora que você já sabe como criar comandos básicos e avançados, vamos aprender a criar comandos totalmente personalizados para atender às suas necessidades específicas. Aqui estão algumas ideias de comandos que você pode implementar:

### 1. Comando `📜 lyrics` para Mostrar Letras de Músicas

Podemos criar um comando para buscar as letras das 🎶 músicas tocadas. Para isso, podemos usar a API do Genius.

Primeiro, instale a biblioteca `lyricsgenius`:

```bash
pip install lyricsgenius
```

Depois, crie um aplicativo no [Genius API](https://genius.com/developers) para obter sua chave de API.

```python
import lyricsgenius

genius = lyricsgenius.Genius("SUA_API_KEY")

@client.command(name='lyrics')
async def lyrics(ctx, *, track_name: str):
    song = genius.search_song(track_name)
    if song:
        await ctx.send(f'📜 Letra da música "{song.title}":\n{song.lyrics[:2000]}')
    else:
        await ctx.send('Não foi possível encontrar a letra da música.')
```

### 2. Comando `🎶 recommend` para Recomendação de Músicas

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

Este guia mostrou como você pode adicionar funcionalidades incríveis ao seu 🤖 bot de 🎶 música no Discord. Agora seu bot pode:

- 🔊 Mudar volume, silenciar, pausar e retomar músicas.
- 📜 Gerenciar uma fila de músicas com comandos como `queue`, `skip`, `clear_queue`, `shuffle`, e `now_playing`.
- 🌐 Integrar com plataformas populares como Spotify e Deezer.
- 📜 Buscar letras de músicas e fornecer recomendações musicais.
- 🤖 Melhorar a interação com os usuários por meio de mensagens de boas-vindas, emojis e respostas personalizadas.

Você pode continuar expandindo o bot adicionando mais comandos e funcionalidades que fizerem sentido para o seu uso. Divirta-se programando e aprimorando seu bot! Caso precise de mais ideias ou ajuda, estou à disposição para colaborar mais. 😊
