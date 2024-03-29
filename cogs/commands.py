import discord, time, json, os
from discord.ext import commands
from functions import language, config

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def language(self, ctx, arg):
        config["language"] = arg

        i = open("config.json", "w+")
        i.write(json.dumps(config, indents=2))
        i.close()
        return await ctx.send(f'{language["foobar"]} **{arg}**')

    @commands.command()
    async def join(self, ctx):
        server = ctx.guild.id

        if(ctx.author.voice):
            channel = ctx.author.voice.channel
            if channel == ctx.voice_client:
                pass
            elif ctx.voice_client is None:
                async with ctx.typing():
                    await channel.connect()

                f = open(f"files/{server}/channel.txt", "w")
                f.write(f"{ctx.author.voice.channel.id}")
                f.close()
            else:
                async with ctx.typing():
                    await ctx.voice_client.move_to(channel)

                f = open(f"files/{server}/channel.txt", "w")
                f.write(f"{ctx.author.voice.channel.id}")
                f.close()
            return
        else:
            return await ctx.send(f'{language["say"]["error1"]}')

    @commands.command()
    async def leave(self, ctx):
        channel = ctx.author.voice.channel
        if channel != None:
            try:
                await ctx.voice_client.disconnect()
            except:
                pass
        else:
            ctx.send(f'{language["say"]["error3"]}')
        os.remove("files/channel.txt") 
        return

async def setup(bot):
    await bot.add_cog(General(bot))
