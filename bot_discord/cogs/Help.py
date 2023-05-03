import discord
from discord.ext import commands
import io
import traceback

version1="Bot V.0305-23.beta"
version2 ="`test`"

version3="Bot V.2404-23.beta"
version4 ="`Optimisation, vkick command, update helps command`"

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Help.py is ready")
        
    
        
    @commands.command()
    async def helps(self, ctx):
        await ctx.message.delete()

        embed_message = discord.Embed(
            title="Helps",
            description="Toutes les commandes",
            color=discord.Color.random()
        )

        embed_message.set_author(
            name=f"Demandé par {ctx.author.name}",
            icon_url=ctx.author.avatar
        )
        embed_message.set_thumbnail(url=ctx.guild.icon)
        embed_message.add_field(name="helps", value="help show this message =help")
        embed_message.add_field(name="ping", value="ping the bot =ping")
        embed_message.add_field(name="version, v", value="Bot version =version",)
        embed_message.add_field(name="stop", value="stop the bot =stop (only owner)")
        embed_message.add_field(name="clear, prune", value="clear messages =clear [number] (messages perms only) max 70 messages")
        embed_message.add_field(name="kick", value="kick members =kick [@ user or ID] (kick perms only)")
        embed_message.add_field(name="ban", value="ban members =ban [@ user or ID] (ban perms only)")
        embed_message.add_field(name="unban", value="unban members =unban [@ user or ID] (ban perms only)")
        embed_message.add_field(name="spam", value="spam in chat =spam [Number of Times] [Something to say] (admin perms only)")
        embed_message.add_field(name="repeat, say", value="Repeat messages =repeat [Something to repeat]")
        embed_message.add_field(name="8ball, magicball", value="8ball game =8ball [Something to answer]")
        embed_message.add_field(name="hilaire", value="hilaire game =hilaire")
        embed_message.add_field(name="level, lvl", value="level see your ranking =level [@ user]")
        embed_message.add_field(name="resetlevel, rsl", value="resetlevel reset member level =resetlevel [@ user] (messages perms only)")
        embed_message.add_field(name="levelsettings, lvls", value="levelsettings enable or disable leveling system (admins perms only)")
        embed_message.add_field(name="mp, dm", value="mp send mp to user =mp [@ user] (admins perms only)")
        embed_message.add_field(name="deldms, delmp", value="deldms clear dms with bot =deldms (admin perms only)")
        embed_message.add_field(name="slist", value="slist list all soundboard =slist 4")
        embed_message.add_field(name="splay", value="splay make play soundboard =splay [number]")
        embed_message.add_field(name="sjoin", value="sjoin make join bot =sjoin [need to be in a vc]")
        embed_message.add_field(name="sleave", value="sleave make leave bot =sleave")
        embed_message.add_field(name="sstop", value="stop bot making soundboard =sstop")
        embed_message.add_field(name="srandom", value="srandom play a random soundboard between 1 and 5 minutes =srandom")
        embed_message.add_field(name="srandomskip", value="skip skip random soundboard =srandomskip [only when a sound is playing]")
        embed_message.add_field(name="srandomstop", value="stops stop random soundboard =srandomstop")
        embed_message.add_field(name="vkick", value="vkick kick user in a vc =vkick [@ID] (admin perms only)")
        embed_message.add_field(name="tts", value="tts make bot say something with googletts voice in vc =tts [langue] [texte]")
        embed_message.add_field(name="report", value="report only for report a bug or make a feedback =report [something to send]")
        embed_message.set_footer(text=version1)

        await ctx.send(embed=embed_message)

          
    
    @commands.command(aliases=["v"])
    async def version(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(title="Versions du Bot", color=discord.Color.random())
        embed.set_author(name=f"Demandé par {ctx.author.name}", icon_url=ctx.author.avatar)
        embed.add_field(name="", value="")
        embed.add_field(name="Last Version", value=version1)
        embed.add_field(name="Update Logs", value=version2)
        embed.add_field(name="", value="")
        embed.add_field(name="Old Version", value=version3)
        embed.add_field(name="Update Logs", value=version4)
        embed.add_field(name="", value="")
        embed.add_field(name="Preview Version", value="Bot V.0103-23.alpha")
        embed.add_field(name="Update Logs", value="`Optimisation, First update and alot of new command`")
        embed.add_field(name="Date format", value="`MM/DD/YY`")
        with open("./Autres/hilaire.png", "rb") as f:
            image_data = f.read()
        embed.set_thumbnail(url="attachment://hilaire.png")
        await ctx.send(embed=embed, file=discord.File(io.BytesIO(image_data), "hilaire.png"))
        
    @commands.command()
    async def ping(self, ctx):
        await ctx.message.delete()
        bot_latency = round(self.client.latency * 1000)
        
        embed = discord.Embed(title=f"Pong! {bot_latency} ms.", color=discord.Color.random())
        embed.set_author(name=f"Demandé par {ctx.author.name}", icon_url=ctx.author.avatar)
        embed.set_footer(text=version1)
        await ctx.send(embed=embed)


            
async def setup(client):
    await client.add_cog(Help(client))