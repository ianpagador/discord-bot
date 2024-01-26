import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import yt_dlp as youtube_dl
import json
import requests
import pandas as pd

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)

load_dotenv()
df = pd.read_csv('name_id.csv')

insult_status = False

def getInsult(name):
  response = requests.get("https://insult.mattbas.org/api/insult.json?who=" + name)
  json_data = json.loads(response.text)
  insult = json_data["insult"]
  return insult

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
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
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
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

@bot.event
async def on_ready():
  print("We have logged in as {0.user}".format(bot))

@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("connect to vc dummy")
        return
    else:
        channel = ctx.author.voice.channel
    await channel.connect()

@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()

@leave.error
async def leave_error(ctx, error: discord.DiscordException):
    if isinstance(error, commands.CommandError):
        await ctx.send("i'm not in vc stupid")
    else:
        raise error

@bot.command(name='play_song', help='To play song')
async def play(ctx,url):
    try:
        server = ctx.message.guild
        voice_channel = server.voice_client
        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
        await ctx.send('**now playing:** {}'.format(filename))
    except:
        await ctx.send("uh oh smth's wrong")

@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()

@pause.error
async def pause_error(ctx, error: discord.DiscordException):
    if isinstance(error, commands.CommandError):
        await ctx.send("im not playing anything goofy")
    else:
        raise error

@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()

@resume.error
async def resume_error(ctx, error: discord.DiscordException):
    if isinstance(error, commands.CommandError):
        await ctx.send("what do you want me to resume lol")
    else:
        raise error

@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()

@stop.error
async def stop_error(ctx, error: discord.DiscordException):
    if isinstance(error, commands.CommandError):
        await ctx.send("nothing was playing are you delulu")
    else:
        raise error

@bot.command(name='insults', help='Turn insults on or off')
async def insults(ctx,status):
    global insult_status
    if status == "on" and insult_status == False:
        insult_status = True
        await ctx.send("i can shit on yall now hehe")
    elif status == "off" and insult_status == True:
        insult_status = False
        await ctx.send("ur no fun but i guess")
    else:
        await ctx.send("that's how it already was stupid")

@bot.event
async def on_message(msg):
  await bot.process_commands(msg)
  if insult_status == True:
      for i in range(0,df.shape[0]):
          if int(df.iloc[i][0]) == int(msg.author.id):
              name = str(df.iloc[i][1])
              insult = getInsult(name)
              await msg.channel.send(insult)
          else:
              raise error

if __name__ == "__main__" :
    bot.run(os.getenv('TOKEN'))