import discord, os, shutil
from discord.ext import commands
from discord import FFmpegPCMAudio
from gtts import gTTS
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="'", description="Discord tts bot core", intents=intents)

def checkServerMetadata(message, autor, server):
    txt = open('files/data.txt', 'w')
    if "()" in message:
        txt.write(autor + "()")
    else:
        txt.write(autor)     
    txt.close()
    return
    
def botSetup():
    #Clean Remaning Data
    if os.path.exists("files") == True:
        shutil.rmtree("files")
    #Create new server files    
    os.mkdir("files")
    txt = open('files/data.txt', 'w')
    txt.write("Nobody")
    txt.close()

@bot.event
async def on_ready():
    print(f'{bot.user} O')

@bot.command()
async def ping(ctx, message):
    await ctx.send("PONG!!")
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
            
    txt = open('files/data.txt', 'r+')
    data = txt.read()
    txt.close
    
    if data == "Nobody":
        checkServerMetadata(message, autor, server)    
    elif data == autor:
        autor = "()"
        if "()" in message:
            checkServerMetadata(message, autor, server)        
    elif data != autor:
        checkServerMetadata(message, autor, server)
        
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
    speech.save("./files/audio.mp3")
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
            ctx.voice_client.play(FFmpegPCMAudio("./files/audio.mp3"))
            print("playing audio")
    else:
        await ctx.send("Debes estar en un canal")
        
botSetup()
bot.run(os.getenv('TOKEN'))