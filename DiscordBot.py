
import json
import time
from logging import info
import discord
#from discord.abc import GuildChannel
import urllib.request
from discord import message
import requests
from discord import Embed
import base64
#from discord.message import Message
capes = {
    'http://textures.minecraft.net/texture/2340c0e03dd24a11b15a8b33c2a7e9e32abb2051b2481d0ba7defd635ca7a933': 'Migrator',
    'http://textures.minecraft.net/texture/953cac8b779fe41383e675ee2b86071a71658f2180f56fbce8aa315ea70e2ed6': 'Minecon 2011',
    'http://textures.minecraft.net/texture/a2e8d97ec79100e90a75d369d1b3ba81273c4f82bc1b737e934eed4a854be1b6': 'Minecon 2012',
    'http://textures.minecraft.net/texture/153b1a0dfcbae953cdeb6f2c2bf6bf79943239b1372780da44bcbb29273131da': 'Minecon 2013',
    'http://textures.minecraft.net/texture/b0cc08840700447322d953a02b965f1d65a13a603bf64b17c803c21446fe1635': 'Minecon 2015',
    'http://textures.minecraft.net/texture/e7dfea16dc83c97df01a12fabbd1216359c0cd0ea42f9999b6e97c584963e980': 'Minecon 2016',
    'http://textures.minecraft.net/texture/17912790ff164b93196f08ba71d0e62129304776d0f347334f8a6eae509f8a56': 'Realms Mapmaker',
    'http://textures.minecraft.net/texture/5786fe99be377dfb6858859f926c4dbc995751e91cee373468c5fbf4865e7151': 'Mojang',
    'http://textures.minecraft.net/texture/1bf91499701404e21bd46b0191d63239a4ef76ebde88d27e4d430ac211df681e': 'Translator',
    'http://textures.minecraft.net/texture/ae677f7d98ac70a533713518416df4452fe5700365c09cf45d0d156ea9396551': 'Mojira Moderator',
}

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('hello'):
        await message.channel.send('Hello, how are you?')

    if message.content.startswith('!emojitest'):
        await message.channel.send(':mvp3:')

    if message.content.startswith('hi'):
        await message.channel.send('Hello, how are you?')

    if message.content.startswith('how are you'):
        await message.channel.send('Being a bot LOL')

    if message.content.startswith('!embed'):
        await message.channel.send(embed= Embed(title= 'Username | Minecraft Profile', description= 'Info about profile'))

    if message.content.startswith('!rainbow'):
        await message.channel.send('Red, Orange, Yellow, Green, Blue, Indigo, Violet')

    if message.content.startswith('!purge'):
        await message.channel.purge(limit = int(message.content.split(' ')[1]))

    if message.content.startswith('!help'):
        await message.channel.send(''' 
**My Commands:**

!ign

!rainbow

!purge

!embed

**More To Come!**
        ''')
    
    if message.content.startswith('!ign'):
        m = message.content
        username = m.split(' ')[1]
        #await message.channel.send('https://namemc.com/profile/' + username)
        r = requests.get('https://api.mojang.com/users/profiles/minecraft/' + username)
        if r.status_code != 200:
            e=Embed(title= username, description = 'Username Available, Available Soon Or Blocked')
            await message.channel.send(embed = e)
            return

        if len(username) > 16:
            e=Embed(title= username, description = 'Username Too Long')
            await message.channel.send(embed = e)
            return
        id = r.json()['id']
        r = requests.get('https://sessionserver.mojang.com/session/minecraft/profile/' + id)
        properties = r.json()['properties']
        r = requests.get('https://api.mojang.com/user/profiles/' + id + '/names')
        namehistory = r.json()
        for property in properties:
            data = base64.b64decode(property['value'])
            print(data)
            info = json.loads(data)
            print(info)
            skin = info['textures']['SKIN']['url']
            cape = info['textures'].get('CAPE',{}).get('url','')
            #await message.channel.send('**Profile UUID**: ' + id)
            #await message.channel.send('**Skin:** ' + skin)
            #await message.channel.send('**Cape:** ' + capes[cape])
            #await message.channel.send(cape)
        #await message.channel.send('**Name History: **' + ', '.join([name['name'] for name in namehistory]))
        e=Embed(title= namehistory[-1]['name'])
        #e.add_field(name='changed at:', value='<t:' + str(int(int(namehistory[-1]['changedToAt'])/1000)) + '>', inline=False)
        e.add_field(name= 'UUID:', value=id, inline=True)
        e.add_field(name= 'Active Cape:', value=capes.get(cape,'None'), inline=False)
        history = '\n'.join(x['name'] + ': <t:' + str(int(int(x.get('changedToAt', 0))/1000)) + ':d>' for x in namehistory)
        e.add_field(name='Name History:', value=history)
        e.add_field(name='Skin Download:', value='https://crafatar.com/skins/' + id , inline=False)
        e.set_thumbnail(url='https://crafatar.com/renders/body/'+ id)
        await message.channel.send(embed=e)
        #
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

print('Starting...')
client.run('[BOT TOKEN]')