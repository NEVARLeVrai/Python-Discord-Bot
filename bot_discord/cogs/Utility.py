import discord
from discord.ext import commands
import random
import io
import asyncio
from cogs import Help
import traceback


class utility(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    def is_bot_dm(message):
        return message.author.bot and isinstance(message.channel, discord.DMChannel)
    
    def is_bot_dm(self, message):
        return message.author == self.client.user and isinstance(message.channel, discord.DMChannel)

    async def send_tts(self, vc, lang, vol, text):
        # Découpe le texte en parties de longueur maximale max_length
        max_length = 200
        text_parts = [text[i:i+max_length] for i in range(0, len(text), max_length)]

        # Joue chaque partie du texte
        for part in text_parts:
            vc.play(discord.FFmpegPCMAudio(
                executable="C:/ProgramData/chocolatey/lib/ffmpeg-full/tools/ffmpeg/bin/ffmpeg.exe",
                source=f"http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl={lang}&q={part}",
                options=f"-af volume={vol}"
            ))
            while vc.is_playing():
                await asyncio.sleep(1)



    @commands.Cog.listener()
    async def on_ready(self):
        print("Utility.py is ready")




    @commands.command()
    async def tts(self, ctx, lang="fr",vol="3.0" , *, text):
        await ctx.message.delete()
        vc = None
        if ctx.author.voice:
            vc = await ctx.author.voice.channel.connect()
        else:
            embed5 = discord.Embed(title="TTS Play", description="Vous devez être dans un salon vocal pour utiliser cette commande.", color=discord.Color.red())
            embed5.set_author(name=f"Demandé par {ctx.author.name}", icon_url=ctx.author.avatar)
            embed5.set_footer(text=Help.version1)
            await ctx.send(embed=embed5, delete_after=5)
            return

        embed1 = discord.Embed(title="TTS Play", color=discord.Color.green())
        embed1.set_author(name=f"Demandé par {ctx.author.name}", icon_url=ctx.author.avatar)
        embed1.add_field(name="Volume:", value=f"**{vol}**")
        embed1.add_field(name="Langue:", value=f"**{lang}**")
        embed1.add_field(name="Dit:", value=f"**{text}**", inline=False)
        embed1.set_footer(text=Help.version1)
        await ctx.send(embed=embed1, delete_after=15)
        await self.send_tts(vc, lang, vol , text)
        
        
        await vc.disconnect()
        embed3 = discord.Embed(title="TTS Play", description=f"Déconnecté avec succés!", color=discord.Color.green())
        embed3.set_author(name=f"Demandé par {ctx.author.name}", icon_url=ctx.author.avatar)
        embed3.set_footer(text=Help.version1)
        await ctx.send(embed=embed3, delete_after=5)







    
    @commands.command(aliases=["8ball"])
    async def magicball(self, ctx, * ,question):
        await ctx.message.delete()
        responses=['Comme je le vois oui.',
                  'Oui.',
                  'Positif',
                  'De mon point de vue, oui',
                  'Convaincu.',
                  'Le plus probable.',
                  'De grandes chances',
                  'Non.',
                  'Négatif.',
                  'Pas convaincu.',
                  'Peut-être.',
                  'Pas certain',
                  'Peut-être',
                  'Je ne peux pas prédire maintenant.',
                  'Je suis trop paresseux pour prédire.',
                  'Je suis fatigué. *continue à dormir*']
        response = random.choice(responses)
        embed=discord.Embed(title="La Boule Magique 8 à parlé!", color=discord.Color.purple())
        embed.set_author(name=f"Demandé par {ctx.author.name}", icon_url=ctx.author.avatar)
        embed.add_field(name='Question: ', value=f'{question}')
        embed.add_field(name='Réponse: ', value=f'{response}')
        embed.set_footer(text=Help.version1)
        with open("./Autres/8ball.png", "rb") as f:
            image_data = f.read()
        embed.set_thumbnail(url="attachment://8ball.png")
        await ctx.send(embed=embed, file=discord.File(io.BytesIO(image_data), "8ball.png"))

            
    @commands.command()
    async def hilaire(self, ctx):
        await ctx.message.delete()
        responses = ["le protocole RS232",
                "FTTH",
                "Bit de Start",
                "Bit de parité",
                "Sinusoïdale",
                "RJ45",
                "Trop dbruiiiit!!!!",
                "Raphaël les écouteurs",
                "Can le téléphone",
                "JoOoAnnY",
                "Le théorème de demorgan"]
        responses = random.choice(responses)
        embed=discord.Embed(title="Wiliam Hilaire à parlé!", color=discord.Color.purple())
        embed.set_author(name=f"Demandé par {ctx.author.name}", icon_url=ctx.author.avatar)
        embed.add_field(name='Hilaire à dit: ', value=f'{responses}')
        embed.set_footer(text=Help.version1)
        with open("./Autres/hilaire.png", "rb") as f:
            image_data = f.read()
        embed.set_thumbnail(url="attachment://hilaire.png")
        await ctx.send(embed=embed, file=discord.File(io.BytesIO(image_data), "hilaire.png"))
    

            
    @commands.command(aliases=["repeat"])
    async def say(self, ctx, *, message,):
        await ctx.message.delete()
        await ctx.send(message)
    
    @commands.command(aliases=["dm"])
    @commands.has_permissions(administrator=True)
    async def mp(self, ctx, user: discord.User, *, message: str):
        
        await ctx.message.delete()
        await user.send(message)

        embed=discord.Embed(title="Message Privé!", description=f"Message envoyé à **{user.name}#{user.discriminator}**", color=discord.Color.gold())
        embed.set_author(name=f"Demandé par {ctx.author.name}", icon_url=ctx.author.avatar)
        embed.set_footer(text=Help.version1)
    
        await ctx.send(embed=embed, delete_after=10)
        
        

    @commands.has_permissions(administrator=True)
    @commands.command(aliases=["deldms"])
    async def delmp(self, ctx):
        await ctx.message.delete()
        try:
            total_deleted = 0
            deleted_messages = {}  # dictionnaire pour stocker le nombre de messages supprimés par utilisateur

            # envoyer un message global indiquant que la suppression des DMs est en cours
            embed = discord.Embed(title="Suppression des messages privés en cours...", color=discord.Color.yellow())
            embed.set_footer(text=Help.version1)
            await ctx.send(embed=embed, delete_after=10)

            tasks = []
            for member in ctx.guild.members:
                if not member.bot:
                    dm_channel = await member.create_dm()
                    messages = [msg async for msg in dm_channel.history() if self.is_bot_dm(msg)]
                    if messages:
                        deleted_count = await dm_channel.send('\n'.join(f"Suppression de {msg.content}..." for msg in messages))
                    else:
                        deleted_count = None
                    if deleted_count is not None:
                        await deleted_count.delete()
                    messages_to_delete = [msg async for msg in dm_channel.history() if self.is_bot_dm(msg)]
                    deleted_count = len(messages_to_delete)
                    total_deleted += deleted_count
                    if deleted_count > 0:
                        deleted_messages[member.name] = deleted_count  # stocker le nombre de messages supprimés par utilisateur
                    tasks.append(asyncio.gather(*[msg.delete() for msg in messages_to_delete]))

                    # envoyer un message individuel pour chaque utilisateur dont les DMs ont été supprimés
                    if deleted_count > 0:
                        embed = discord.Embed(title=f"Messages privés de **{member.name}#{member.discriminator}** supprimés !", color=discord.Color.green())
                        embed.add_field(name="Nombre de messages supprimés", value=str(deleted_count))
                        embed.set_footer(text=Help.version1)
                        tasks.append(ctx.send(embed=embed, delete_after=10))

            # attendre que toutes les tâches soient terminées
            await asyncio.gather(*tasks)

            # envoyer un message global indiquant le nombre total de messages supprimés
            if total_deleted > 0:
                embed = discord.Embed(title=f"Messages privés supprimés au total.", description=f"{total_deleted}", color=discord.Color.purple())
            else:
                embed = discord.Embed(title="Aucun message privé à supprimer.", color=discord.Color.red())
            embed.set_footer(text=Help.version1)
            await ctx.send(embed=embed, delete_after=10)
        except Exception as e:
            traceback.print_exc()

           
    @tts.error
    async def tts_error(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, commands.MissingRequiredArgument):
            embed2 = discord.Embed(title= "TTS Erreur", description="Syntaxe : =tts [langue] [volume ex= 3.0] <texte>", color=discord.Color.yellow())
            embed2.set_author(name=f"Demandé par {ctx.author.name}", icon_url=ctx.author.avatar)
            embed2.set_footer(text=Help.version1)
            await ctx.send(embed = embed2, delete_after=10)        
            
    


async def setup(client):
    await client.add_cog(utility(client))