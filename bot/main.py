# Рассказать что такое декораторы
# Что такое api и с чем его едят
import random
import discord
import requests


TOKEN = 'ODQwNDc2OTEwNjA1MDQxNzA0.GgEz-X.yWPkl6OLAU5I8eUMV67uqToVcFw4Ata2ycyplQ'
SERVER_NAME = 'Сергей МЛ'
IMG_EXTENTIONS = ['jpg', 'png', 'jpeg']
RULES = {'камень': 'бумага',
         'ножницы': 'камень',
         'бумага': 'ножницы'}

client = discord.Client(intents=discord.Intents.default())


def request_api_data(url, filename):
    data = {"url": url, "filename": filename}
    url = "http://104.236.235.5:5000/predict"
    response = requests.post(url, data)
    if response.status_code == 200:
        label = response.json()['class_name']
        return label
    return 'Произошла ошибка при запросе данных'


@client.event
async def on_ready():
    for guild in client.guilds:
        print(guild)


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if len(message.attachments) == 1:
        attachment = message.attachments[0]
        ext = attachment.filename.split('.')[-1]
        if ext in IMG_EXTENTIONS:
            data = request_api_data(attachment.url, attachment.filename)
            await message.channel.send(data)

    if message.content.lower() in RULES.keys():
        computer = random.choice(list(RULES.keys()))

        await message.channel.send(computer)

        if message.content.lower() == computer:
            await message.channel.send('Ничья')    
        elif message.content.lower() == RULES[computer]:
            await message.channel.send('Ты победил')    
        else:
            await message.channel.send('Ты проиграл')   

client.run(TOKEN)
