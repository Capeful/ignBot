
import json
from math import pi
import time
from logging import info
import discord
#from discord.abc import GuildChannel
import urllib.request
import requests
from discord import Embed
import base64


from PIL import Image
from io import BytesIO
print(discord.Color.red())
print(discord.Color.green())
print(discord.Color.blue())

#Finds main colour for embed
def compute_average_image_color(img):
    width, height = img.size

    counts = {}
    max=0
    color=(0,0,0)
    for x in range(0, width):
        for y in range(0, height):
            r, g, b, a = img.getpixel((x,y))
            if (r,g,b) == (0,0,0):
                continue
            counts[(r,g,b)] = counts.get((r,g,b),0)+1
            if counts[(r,g,b)]>max:
                max=counts[(r,g,b)]
                color=(r,g,b)
    return color
#List of capes:
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
    'http://textures.minecraft.net/texture/9e507afc56359978a3eb3e32367042b853cddd0995d17d0da995662913fb00f7': 'Mojang Studios',
    'http://textures.minecraft.net/texture/ca35c56efe71ed290385f4ab5346a1826b546a54d519e6a3ff01efa01acce81': 'Cobalt',
    'http://textures.minecraft.net/texture/8f120319222a9f4a104e2f5cb97b2cda93199a2ee9e1585cb8d09d6f687cb761': 'Mojang (Classic)',
    'http://textures.minecraft.net/texture/3efadf6510961830f9fcc077f19b4daf286d502b5f5aafbd807c7bbffcaca245': 'Scrolls'
}

client = discord.Client()

@client.event
async def on_message(message: discord.Message):
#    if message.author == client.user:
 #       return

  #  if message.content.startswith('hello'):
   #     await message.channel.send('Hello, how are you?')

    #if message.content.startswith('!etest'):
        #await message.channel.send('<:nyancat:943592179371221106>')

    #if message.content.startswith('hi'):
     #   await message.channel.send('Hello, how are you?')

   # if message.content.startswith('how are you'):
    #    await message.channel.send('Being a bot LOL')

   # if message.content.startswith('!embed'):
    #    await message.channel.send(embed= Embed(title= 'Username | Minecraft Profile', description= 'Info about profile'))

    if message.content.startswith('!rainbow'):
        await message.channel.send('Red, Orange, Yellow, Green, Blue, Indigo, Violet')

    if message.content.startswith('!test'):
        await message.channel.send(client.guilds)

    if message.content.startswith('!embtest'):
        await message.channel.send(client.guilds)

    if message.content.startswith('!purge'):
        print([x.name for x in message.author.roles])
        if 'purgePerms' in [x.name for x in message.author.roles]:
            await message.channel.purge(limit = int(message.content.split(' ')[1]))

    if message.content.startswith('!help'):
        await message.channel.send(''' 

Hi, I was created by Capeful#3176

**My Commands:**

!ign

!rainbow

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
        r = requests.get('https://api.gapple.pw/cors/optifine/' + namehistory[-1]['name'])
        capeOF = r.status_code
        if r.status_code==200:
            capeOF='https://api.gapple.pw/cors/optifine/' + namehistory[-1]['name']
        else:
            capeOF='No cape found'
        r = requests.get('https://api.gapple.pw/status/' + id)
        accType = r.json()['status']
        if accType =='new_msa':
            accType='New Microsoft Account (MSA)'
        if accType==migrated_msa:
            accType='Migrated From Mojang Account (MSA)'
        if accType==migrated_msa_from_legacy:
            accType='Migrated From Legacy Account (MSA)'
        if accType==msa:
            accType='Unsure What Type Of MSA'
        if accType==mojang:
            accType='Mojang Account'
        if accType==legacy:
            accType='Legacy Account'


        for property in properties:
            data = base64.b64decode(property['value'])
            print(data)
            info = json.loads(data)
            print(info)
            skin = info['textures']['SKIN']['url']
            model = info ['textures']['SKIN'].get('metadata',{}).get('model','')
            if model=='slim':
                model = 'Slim (Alex)'
            else: 
                model = 'Regular (Steve)'
            
            cape = info['textures'].get('CAPE',{}).get('url','')
            #capeOF = ('https://api.gapple.pw/cors/optifine/' + namehistory[-1]['name'])
            #await message.channel.send('**Profile UUID**: ' + id)
            #await message.channel.send('**Skin:** ' + skin)
            #await message.channel.send('**Cape:** ' + capes[cape])
            #await message.channel.send(cape)
            #await message.channel.send('**Name History: **' + ', '.join([name['name'] for name in namehistory]))
        
        img=requests.get('https://visage.surgeplay.com/full/'+ id)
        file_jpgdata = BytesIO(img.content)
        pic = Image.open(file_jpgdata)
        (r,g,b) = compute_average_image_color(pic)

        e=Embed(title= namehistory[-1]['name'], color=discord.Color.from_rgb(r,g,b))
        e.set_thumbnail(url='https://visage.surgeplay.com/full/'+ id)
        #e.add_field(name='changed at:', value='<t:' + str(int(int(namehistory[-1]['changedToAt'])/1000)) + '>', inline=False)
        e.add_field(name= 'UUID:', value=id, inline=False)
        e.add_field(name= 'Current Cape:', value=capes.get(cape,'None'), inline=True)
        if capeOF=='No cape found':
            e.add_field(name= 'Optifine Cape', value=capeOF, inline=True)

        else:
            e.add_field(name= 'Optifine Cape', value='[Click Here!]({})'.format(capeOF), inline=True)

        name_history_string = []
        for name in namehistory:
            changedAt = int(int(name.get('changedToAt', 0))/1000)
            if changedAt > 0:
                name_history_string.append(name['name'] + ': <t:' + str(changedAt) + ':d>')
            else:
                 name_history_string.append(name['name'] + ': (First IGN)')
        history = '\n'.join(name_history_string)
        e.add_field(name='Name History:', value=history, inline=False)
        e.add_field(name='Account Type:', value=accType, inline=True)        
        e.add_field(name= 'Skin Type:', value=model, inline=True)
        e.add_field(name='Skin Download:', value='[Click Here!](https://crafatar.com/skins/{})'.format(id), inline=False)
        e.add_field(name="NameMC", value='[Click Here!](https://namemc.com/profile/{})'.format(namehistory[-1]['name']), inline=True)

        await message.channel.send(embed=e)
        

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    game = discord.Game("https://bit.ly/31uQAGf")
    listen = discord.Activity(type=discord.ActivityType.listening, name= '!help')
    await client.change_presence(status=discord.Status.online, activity=listen)

print('Starting...')
client.run('BOT_TOKEN_HERE')
