# bot.py
import discord
import os
import youtube_dl
import asyncio
from datetime import datetime
from youtube_dl import YoutubeDL
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') # token fora do codigo por seguranca e vulnerabilidade

intents = discord.Intents().all()

client = commands.Bot(command_prefix='.', intents=intents, help_command=None) # prefixo "." para comandos
client.remove_command('help') # remove o comando help (para colocar um personalizado posteriormente)


# start
@client.event
async def on_ready():
    print(f'{client.user.name} está no discord.')
    await client.change_presence(activity=discord.Activity(status=discord.Status.online,
                                                           type=discord.ActivityType.listening,
                                                           name='\".help\"')) # status no discord para o bot


# bem-vindo
@client.event
async def on_member_join(member):
    embedvar = discord.Embed(color=0x00B2E3, timestamp=datetime.now())
    embedvar.add_field(name='Aumentamos a tropa',
                       value=f'{member.mention} bem-vindo(a) à Realeza. :crown: :crocodile:')  # cria o embed
    await client.get_channel(892962718129221654).send(embed=embedvar)  # envia o embed
    await member.add_roles(member.guild.get_role(893618254466138162))  # adiciona o cargo ao novo membro


# comando oi
@client.command()
async def oi(ctx):
    await ctx.send('coe')


# comando gostosa
@client.command()
async def gostosa(ctx):
    await ctx.send('https://cdn.discordapp.com/attachments/709526517864202271/'
                   '905535914699264030/2A98BF6F-E6DF-4034-9B6C-1F82DC6A3519.jpg')
    await ctx.send('Tem dono talarico safado. :face_with_symbols_over_mouth:')


# comando nenem
@client.command()
async def nenem(ctx):
    await ctx.send('https://cdn.discordapp.com/attachments/709526517864202271/893121455880020019/image1.jpg')
    await ctx.send('Faz carinho no neném. :pleading_face:')


# comando purge
@client.command(aliases=['purge'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx):
    await ctx.channel.purge(limit=1000000)


# comando help
@client.command()
async def help(ctx):
    embedvar = discord.Embed(title="Comandos",
                             description="",
                             color=0x9600FF,
                             url='https://github.com/lilrau/lacostinho/blob/main/comandos')
    embedvar.add_field(name="help", value="Mostra esta mensagem.\n ", inline=False)
    embedvar.add_field(name="oi", value="Diga \"oi\" para o Lacostinho!\n ", inline=False)
    embedvar.add_field(name="gostosa", value="Mostra uma gostosa.\n ", inline=False)
    embedvar.add_field(name="nenem", value="Mostra um neném.\n ", inline=False)
    embedvar.add_field(name="purge", value="Limpa as mensagens do canal.\n ", inline=False)
    embedvar.add_field(name="join", value="Traz o bot para seu canal de voz.\n ", inline=False)
    embedvar.add_field(name="leave", value="Retira o bot de seu canal de voz.\n ", inline=False)
    embedvar.add_field(name="play", value="Toca a música escolhida.\n ", inline=False)
    embedvar.add_field(name="pause", value="Pausa a música atual.\n ", inline=False)
    embedvar.add_field(name="resume", value="Continua a música pausada.\n ", inline=False)
    embedvar.add_field(name="stop", value="Para a música.\n ", inline=False)
    embedvar.set_footer(
        text="Atualizado por raulzinho  •  01/10/2021",
        icon_url='https://cdn.discordapp.com/attachments/709526517864202271/893127205822013520/image0.jpg')
    embedvar.set_image(
        url='https://cdn.discordapp.com/attachments/709526517864202271/893142073220403220/comandos_bot_wpp.png')
    await ctx.send(embed=embedvar)


youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '00.000.000.000'  # ipv4
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
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # pega o primeiro item da playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename


# comando join
@client.command(name='join')
async def join(ctx):
    if not ctx.message.author.voice: # erro usuario nao esta em um canal de voz
        await ctx.send("{} não está em um canal de voz.".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()


# comando leave
@client.command(name='leave')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else: # erro bot nao esta em um canal de voz
        await ctx.send("O bot não está conectado em um canal de voz.")


# comando play
# necessita de ffmpeg (?)
@client.command()
async def play(ctx, url):
    ydl_options = {'format': 'bestaudio', 'noplaylist': 'True'}
    ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        with YoutubeDL(ydl_options) as ydl:
            info = ydl.extract_info(url, download=False)
        url = info['formats'][0]['url']
        voice.play(FFmpegPCMAudio(url, **ffmpeg_options, executable='C:\\FFmpeg\\bin\\ffmpeg.exe'))
        voice.is_playing()
    else: # erro ja possui uma musica tocando
        await ctx.send("Uma música já está sendo tocada.")
        return


# comando pause
@client.command(name='pause')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else: # erro nao tem musica sendo tocada
        await ctx.send("O bot não está tocando nada no momento.")


# comando resume
@client.command(name='resume')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else: # erro nao tem musica sendo tocada
        await ctx.send("O bot não estava tocando nada. Use o comando *\".play\"*")


# comando stop
@client.command(name='stop')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:  # erro nao tem musica sendo tocada
        await ctx.send("O bot não está tocando nada no momento")


if __name__ == '__main__':
    client.run(TOKEN) # token fora do codigo por seguranca e vulnerabilidade
