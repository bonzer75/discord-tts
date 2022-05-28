import discord
import os
from discord.ext import commands
from discord import FFmpegPCMAudio
from gtts import gTTS
from dotenv import load_dotenv
import shutil

bot = commands.Bot(command_prefix = "'", description = "Test bot")

def check(message, autor, server):
    txt = open('files/%s/data.txt' % server, 'w')
    if "()" in message:
        txt.write(autor + "()")
    else:
        txt.write(autor)     
    txt.close()
    return
    
def setup():
    if os.path.exists("files") == True:
        shutil.rmtree("files")
        
    os.mkdir("files")
    
    for server in bot.guilds:
        os.mkdir("files/%s" % server.id)
        
        txt = open('files/%s/data.txt' % server.id, 'w')
        txt.write("Nobody")
        txt.close()

@bot.command()
async def say(ctx, *, message):
    autor = ctx.message.author.name
    server = ctx.message.guild.id
        #check if bot is talking
    if ctx.voice_client is None:
        pass
    else:
        if (ctx.voice_client.is_playing()):
            await ctx.send("espera a que termine de hablar")
            
    txt = open('files/%s/data.txt' % server, 'r+')
    data = txt.read()
    txt.close
    
    if data == "Nobody":
        check(message, autor, server)    
    elif data == autor:
        autor = "()"
        if "()" in message:
            check(message, autor, server)        
    elif data != autor:
        check(message, autor, server)
        
    if message == None:
        message = "Hola, me llamo super alexia"
    
    #anonimous message
    if ("()" in message) or ("()" in autor):
        pass
    else:
        message = "%s dice. %s" % (autor, message)
    #new message
    print(message)
    #brasilian voice
    if "ç" in message:
        speech = gTTS(text = message, lang = "pt", slow = False)
    else:
        speech = gTTS(text = message, lang = "es", slow = False)
    #create audio
    speech.save("./files/%s/audio.mp3" % server)
    print("created file")
    #check voice channel
    if(ctx.author.voice):
        channel = ctx.author.voice.channel
        #condiciones
        if channel == ctx.voice_client:
            pass
        elif ctx.voice_client is None:
            await channel.connect()
        else:
            await ctx.voice_client.move_to(channel)
        #voice = await channel.connect()
        if "@" in message:
            await ctx.send("No me hagas mencionar a usuarios, por favor")
        else:
            ctx.voice_client.play(FFmpegPCMAudio("./files/%s/audio.mp3" % server))
            print("playing audio")
    else:
        await ctx.send("Debes estar en un canal")

@bot.command(pass_context = True)
async def join(ctx):
    if(ctx.author.voice):
        channel = ctx.author.voice.channel
        #condiciones
        if(channel == ctx.voice_client):
            pass
        elif(ctx.voice_client is None):
            await channel.connect()
        else:
            await ctx.voice_client.move_to(channel)
    else:
        await ctx.send("Debes estar en un canal de voz")

@bot.command()
async def leave(ctx):
    named = str(ctx.author.voice.channel)
    channel = discord.utils.get(ctx.guild.channels, name=named)
    
    members = []
    
    for i in channel.members:
       members.append(i.name)

    print(members)
    
    if len(members) > 1:
        pass
    else:
        #await channel.connect()
        pass

@bot.command()
async def ping(ctx):
    return print(ctx.message.guild.id)

@bot.event
async def on_ready():
    await bot.change_presence(activity = discord.Streaming(name = "Nuestra Señora de Paris", url = "https://www.twitch.tv/robtop"))
    
    setup()
    return print("bot running")

if os.path.exists("token.txt") == True:
    temp_variable = open('token.txt','r').readlines()
    bot.run(temp_variable[0])
else:
    load_dotenv()
    bot.run(os.environ['TOKEN'])

