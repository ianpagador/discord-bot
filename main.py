import discord
import random
import requests
import os
import json
import time
import pandas as pd

intents = discord.Intents.all()
intents.message_content = True

client = discord.Bot(command_prefix='!', intents=intents)

load_dotenv()
df = pd.read_csv('name_id.csv')
insult_status = False

ballList = [
    "https://media.giphy.com/media/3orieYvhT5EVfSFyBa/giphy.gif",
    "https://media.giphy.com/media/3orifhNhn840GpMMPm/giphy.gif",
    "https://media.giphy.com/media/xT5LMPGVX5evt3MU1i/giphy.gif",
    "https://media.giphy.com/media/3orifcCRUXkwSsCikg/giphy.gif",
    "https://media.giphy.com/media/xT5LMqFOUOHv4kMm8U/giphy.gif"
]


def getJoke():
    response = requests.get(
        "https://v2.jokeapi.dev/joke/Any?blacklistFlags=racist,sexist&type=twopart")
    json_data = json.loads(response.text)
    setup = json_data["setup"]
    punchline = json_data["delivery"]
    totalJoke = setup + "-" + punchline
    return totalJoke


def getQuote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    author = " -" + json_data[0]["a"]
    quote = json_data[0]["q"]
    answer = quote + author
    return answer
    return response

def getInsult(name):
    response = requests.get("https://insult.mattbas.org/api/insult.json?who=" + name)
    json_data = json.loads(response.text)
    insult = json_data["insult"]
    return insult

def randomCat():
    response = requests.get("https://api.thecatapi.com/v1/images/search")
    json_data = json.loads(response.text)
    image = json_data[0]["url"]
    return image

def findDigit(inputMessage):
  digitList = []
  for c in inputMessage:
    c.isdigit()
    if c.isdigit() == True:
      digitList.append(c)
      print(digitList)
    elif c.isdigit() == False:
      stringDigits = [str(i) for i in digitList]
      digitString = "".join(stringDigits)
      numRoll = int(digitString)
      print(numRoll)
      return numRoll

def findStr(inputMessage):
  inputList = [str(inputMessage)]
  strList = []
  for char in inputList:
   for c in char:
       strList.append(c)
  print(strList)
  strCondition = False
  while not strCondition:
    for c in inputMessage:
      c.isdigit()
      if c.isdigit() == True:
        print(strList)
        del strList[0]
        strCondition = False
      elif c.isdigit() == False:
        print(strList)
        stringAll = [str(i) for i in strList]
        inputString = "".join(stringAll)
        print(inputString)
        return inputString
        break

def encrypt(numRoll, inputString):
    newStuff = ""
    for c in inputString:
      textEncrypt = ord(c) + numRoll
      newStuff += chr(textEncrypt)
    return newStuff

def decrypt(numRoll, inputString):
    newerStuff = ""
    for c in inputString:
      textDecrypt = ord(c) - numRoll
      newerStuff += chr(textDecrypt)
    return newerStuff

@client.command(name='insults', help='Turn insults on or off')
async def insults(ctx,status):
    global insult_status
    if status == "on" and insult_status == False:
        insult_status = True
        await ctx.send("i can insult yall now hehe")
    elif status == "off" and insult_status == True:
        insult_status = False
        await ctx.send("ur no fun but i guess")
    else:
        await ctx.send("that's how it already was stupid")

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening, name="!ian"))


def getAge(name):
    webAPI = "https://api.agify.io?name=" + name
    response = requests.get(webAPI)
    json_data = json.loads(response.text)
    age = json_data["age"]
    return age

@client.event
async def on_message(msg):
    await client.process_commands(msg)
    if insult_status == True:
        for i in range(0,df.shape[0]):
            if int(df.iloc[i][0]) == int(msg.author.id):
                name = str(df.iloc[i][1])
                insult = getInsult(name)
                await msg.channel.send(insult)
            else:
                raise error
    elif "POGGERS but text" == msg.content:
        await msg.channel.send("""
    ⠄⠄⠄⠄⠄⠄⣀⣀⣀⣤⣶⣿⣿⣶⣶⣶⣤⣄⣠⣴⣶⣿⣿⣿⣿⣶⣦⣄⠄⠄
    ⠄⠄⣠⣴⣾⣿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦
    ⢠⠾⣋⣭⣄⡀⠄⠄⠈⠙⠻⣿⣿⡿⠛⠋⠉⠉⠉⠙⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿
    ⡎⣾⡟⢻⣿⣷⠄⠄⠄⠄⠄⡼⣡⣾⣿⣿⣦⠄⠄⠄⠄⠄⠈⠛⢿⣿⣿⣿⣿⣿
    ⡇⢿⣷⣾⣿⠟⠄⠄⠄⠄⢰⠁⣿⣇⣸⣿⣿⠄⠄⠄⠄⠄⠄⠄⣠⣼⣿⣿⣿⣿
    ⢸⣦⣭⣭⣄⣤⣤⣤⣴⣶⣿⣧⡘⠻⠛⠛⠁⠄⠄⠄⠄⣀⣴⣿⣿⣿⣿⣿⣿⣿
    ⠄⢉⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣦⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    ⢰⡿⠛⠛⠛⠛⠻⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    ⠸⡇⠄⠄⢀⣀⣀⠄⠄⠄⠄⠄⠉⠉⠛⠛⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    ⠄⠈⣆⠄⠄⢿⣿⣿⣿⣷⣶⣶⣤⣤⣀⣀⡀⠄⠄⠉⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿
    ⠄⠄⣿⡀⠄⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠂⠄⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿
    ⠄⠄⣿⡇⠄⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠄⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿
    ⠄⠄⣿⡇⠄⠠⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠄⠄⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    ⠄⠄⣿⠁⠄⠐⠛⠛⠛⠛⠉⠉⠉⠉⠄⠄⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿
    ⠄⠄⠻⣦⣀⣀⣀⣀⣀⣀⣤⣤⣤⣤⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠄
    """)
    elif "POGGERS" == msg.content:
        await msg.channel.send(
            "https://tenor.com/view/poggers-pepe-gif-12187647")
    elif "OMEGALUL" == msg.content:
        await msg.channel.send(
            "https://tenor.com/view/omegalul-lul-lulw-twitch-emote-gif-13523263"
        )
    elif "KEKW" == msg.content:
        await msg.channel.send(
            "https://tenor.com/view/kekw-twitch-twitchtv-twitch-emote-kek-gif-19085736"
        )
    elif "KEKW but text" == msg.content:
        await msg.channel.send("""
    ⢰⣶⠶⢶⣶⣶⡶⢶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⡶⠶⢶⣶⣶⣶⣶
    ⠘⠄⠄⠄⠄⠄⠄⠄⠄⣿⣿⣿⣿⣿⣿⣿⠿⠄⠄⠄⠈⠉⠄⠄⣹⣶⣿⣿⣿⣿⢿
    ⠄⠤⣾⣿⣿⣿⣿⣷⣤⡈⠙⠛⣿⣿⣿⣧⣀⠠⣤⣤⣴⣶⣿⣿⣿⣿⣿⣿⣿⣿⣶
    ⢠⠄⠄⣀⣀⣀⣭⣿⣿⣿⣶⣿⣿⣿⣿⣿⣿⣤⣿⣿⠉⠉⠉⢉⣉⡉⠉⠉⠙⠛⠛
    ⢸⣿⡀⠄⠈⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⢿⣿⣿⣷⣾⣿
    ⢸⣿⣿⣿⣿⣿⣿⣿⣿⠛⢩⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    ⢸⣿⣿⣿⣿⣿⡿⣿⣿⣴⣿⣿⣿⣿⣄⣠⣴⣿⣷⣭⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    ⠸⠿⣿⣿⣿⠋⣴⡟⠋⠈⠻⠿⠿⠛⠛⠛⠛⠛⠃⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    ⢸⣿⣿⣿⡁⠈⠉⠄⠄⠄⠄⠄⣤⡄⠄⠄⠄⠄⠄⠈⠄⠈⠻⠿⠛⢿⣿⣿⣿⣿⣿
    ⢸⣿⣿⣿⠄⠄⠄⠄⠄⠄⠄⠄⣠⣄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⢀⣀⣿⣿⣿⣿
    ⢸⣿⣿⣿⡀⠄⠄⠄⠄⠄⠄⠄⠉⠉⠁⠄⠄⠄⠄⠐⠒⠒⠄⠄⠄⠄⠉⢸⣿⣿⣿
    ⢸⣿⣿⣿⢿⣦⣄⣠⣄⠛⠟⠃⣀⣀⡀⠄⠄⣀⣀⣀⣀⣀⣀⡀⢀⣰⣦⣼⣿⣿⡿
    ⢸⣿⣿⣿⣿⣿⣿⣻⣿⠄⢰⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢛⣥⣾⣟⣿⣿⣿⣿⣿
    ⢸⣿⣿⣿⣿⣿⣿⣿⣿⡆⠈⠿⠿⠿⠿⠿⠿⠿⠿⠿⣧⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿
    ⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    """)
    elif "COCONUT MALL" == msg.content:
        await msg.channel.send("https://www.youtube.com/watch?v=MoB8QTIvv8E")
        
@bot.command(name='ian', help='that\'s me')
async def ian():
    await msg.channel.send("what's up lol")

@bot.command(name='ianMagic8Ball', help='test your luck')
async def ianMagic8Ball():
    await msg.channel.send(random.choice(ballList))

@bot.command(name='ianInspire', help='feeling down? let me help you')
async def ianInspire():
    quote = getQuote()
    await msg.channel.send(quote)

@bot.command(name='ianJoke', help='feeling sad? let me cheer you up')
async def ianJoke():
    joke = getJoke()
    await msg.channel.send(joke.split("-")[0])
    time.sleep(2)
    await msg.channel.send(joke.split("-")[1])

@bot.command(name='ianNameAge', help='i\'ll guess how old you are based on your name')
async def ianNameAge():
    ms = msg.content
    name = ms[12:]
    print(name)
    age = getAge(name)
    await msg.channel.send(age)
  
@bot.command(name='ianCat', help='i\'ll send a random cat to lighten the mood')
async def ianCat():
    cat = randomCat()
    await msg.channel.send(cat)

@bot.command(name='ianEncrypt', help='create a caesar cipher as follows: !ianEncrypt index message')
async def ianEncrypt():
      ms = msg.content
      length = len("!ianEncrypt")
      inputMessage = ms[length:]
      numRoll = findDigit(inputMessage)
      inputString = findStr(inputMessage)
      encryptAnswer = encrypt(numRoll, inputString)
      await msg.channel.send(encryptAnswer)

@bot.command(name='ianDecrypt', help='decode a caesar cipher as follows: !ianDecrypt index message')
async def ianDecrypt():
      ms = msg.content
      length = len("!ianEncrypt")
      inputMessage = ms[length:]
      numRoll = findDigit(inputMessage)
      inputString = findStr(inputMessage)
      decryptAnswer = decrypt(numRoll, inputString)
      await msg.channel.send(decryptAnswer)
      
if __name__ == "__main__" :
    bot.run(os.getenv('TOKEN'))
