# bot.py
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents().all()

client = commands.Bot(command_prefix='.', intents=intents)


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
async def clear(ctx, member):
    await ctx.channel.purge(limit=1000000)
    await ctx.send(f'Chat do canal limpo por {member.mention}.')



client.run(TOKEN)
