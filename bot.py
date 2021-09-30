# bot.py
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents().all()

client = commands.Bot(command_prefix='.', intents=intents, help_command=None)


# start
@client.event
async def on_ready():
    print(f'{client.user.name} está no discord.')
    game = discord.Game("o crocodilo no peito")
    await client.change_presence(status=discord.Status.online, activity=game)


# bem-vindo
@client.event
async def on_member_join(member):
    await client.get_channel(892962718129221654).send(f'Salve {member.mention}. Bem-vindo(a) à realeza. :sunglasses:')


# comando oi
@client.command()
async def oi(ctx):
    await ctx.send('coe')


# comando gostosa
@client.command()
async def gostosa(ctx):
    await ctx.send('https://cdn.discordapp.com/attachments/709526517864202271/893121455523528734/image0.jpg')
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
async def ajuda(ctx):
    embedVar = discord.Embed(title="Comandos",
                             description="",
                             color=0x9600FF,
                             url='https://github.com/lilrau/lacostinho/blob/main/comandos')
    embedVar.add_field(name="help", value="Mostra esta mensagem.", inline=False)
    embedVar.add_field(name="oi", value="Diga \"oi\" para o Lacostinho!", inline=False)
    embedVar.add_field(name="gostosa", value="Mostra uma gostosa.", inline=False)
    embedVar.add_field(name="nenem", value="Mostra um neném.", inline=False)
    embedVar.add_field(name="purge", value="Limpa as mensagens do canal.", inline=False)
    embedVar.set_footer(
        text="Atualizado por raulzinho  •  30/09/2021",
        icon_url='https://cdn.discordapp.com/attachments/709526517864202271/893127205822013520/image0.jpg')
    embedVar.set_image(
        url='https://cdn.discordapp.com/attachments/709526517864202271/893142073220403220/comandos_bot_wpp.png')
    await ctx.send(embed=embedVar)


client.run(TOKEN)
