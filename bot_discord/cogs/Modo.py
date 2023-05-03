import discord
from discord.ext import commands
import asyncio
from cogs import Help
import traceback
import requests


class Modo(commands.Cog):
    def __init__(self, client):
        self.client = client    
        self.webhook_url = "https://discord.com/api/webhooks/1097171152079704205/J0-Ib9GBFpGhRedu1Qpblot6rAxoHeZGF-tvgCGyazdp_XIeaTyqsAO2lYsL7yEdg3Dv" # Remplacez WEBHOOK_ID et WEBHOOK_TOKEN par les valeurs de votre webhook


    @commands.Cog.listener()
    async def on_ready(self):
        print("Modo.py is ready")


    @commands.command(name="report")
    async def report(self, ctx, *, message: str):
        await ctx.message.delete()
        """Signaler un bug"""
        data = {
            "content": f"**Bug signalé !**\n\nPar: **{ctx.author.name}#{ctx.author.discriminator}**\nID: **{ctx.author.id}**\nMention: {ctx.author.mention}\nContenu: {message}\n\nDev: **<@745923070736465940>**\n**{Help.version1}**"
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(self.webhook_url, json=data, headers=headers)
        if response.status_code == 204:
            embedc = discord.Embed(title="Signalement", description="Merci d'avoir signalé ce bug.", color=discord.Color.green())
            embedc.add_field(name="",value="Nous allons le corriger dès que possible.", inline=False)
            embedc.set_author(name=f"Demandé par {ctx.author.name}", icon_url=ctx.author.avatar)
            embedc.set_footer(text=Help.version1)
            await ctx.send(embed=embedc, delete_after=5)
        else:
            embedc1 = discord.Embed(title="Erreur de signalement.", description="Erreur lors de l'envoi du message.", color=discord.Color.red())
            embedc1.add_field(name="",value="Veuillez réessayer plus tard.", inline=False)
            embedc1.set_author(name=f"Demandé par {ctx.author.name}", icon_url=ctx.author.avatar)
            embedc1.set_footer(text=Help.version1)
            await ctx.send(embed=embedc1, delete_after=5)
        
        
        
    @commands.command(aliases=["prune"])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        max_amount = 70 # limite de suppression de messages
        if amount > max_amount:
            await ctx.send(f"Vous ne pouvez pas supprimer plus de **{max_amount}** messages à la fois.")
            await asyncio.sleep(1) # Attendre une seconde entre chaque envoi de message
            amount = max_amount
        await ctx.channel.purge(limit=amount+1)
        await asyncio.sleep(1) # Attendre une seconde entre chaque envoi de message
        await ctx.send(f"**{amount}** messages ont été supprimés.", delete_after=10)

        
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, modreaseon):
        await ctx.message.delete()
        embed = discord.Embed(title="Vous avez été kick!", description=f"Vous avez été kick de **{ctx.guild.name}** par {ctx.author.mention} pour la raison suivante: **{modreaseon}**", color=discord.Color.yellow())
        embed.set_author(name=f"Demandé par {ctx.author.name}", icon_url=ctx.author.avatar)
        embed.set_footer(text=Help.version1)
        await member.send(embed=embed)
        await ctx.guild.kick(member)
        
        conf_embed = discord.Embed(title= "Réussi!", description="", color=discord.Color.yellow())
        conf_embed.set_author(name=f"Demandé par {ctx.author.name}", icon_url=ctx.author.avatar)
        conf_embed.add_field(name="Expulsé:", value=f"{member.mention} à été kick par {ctx.author.mention}.", inline=False)
        conf_embed.add_field(name="Raison:", value=modreaseon, inline=False)
        conf_embed.set_footer(text=Help.version1)
        
        await ctx.send(embed=conf_embed)
        
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, modreaseon):
        await ctx.message.delete()
        embed = discord.Embed(title="Vous avez été banni!", description=f"Vous avez été banni de **{ctx.guild.name}** par {ctx.author.mention} pour la raison suivante: **{modreaseon}**", color=discord.Color.red())
        embed.set_author(name=f"Demandé par {ctx.author.name}", icon_url=ctx.author.avatar)
        embed.set_footer(text=Help.version1)
        await member.send(embed=embed)
        await ctx.guild.ban(member)

        conf_embed = discord.Embed(title= "Réussi!", description="", color=discord.Color.red())
        conf_embed.set_author(name=f"Demandé par {ctx.author.name}", icon_url=ctx.author.avatar)
        conf_embed.add_field(name="Banni:", value=f"{member.mention} a été banni par {ctx.author.mention}.", inline=False)
        conf_embed.add_field(name="Raison:", value=modreaseon, inline=False)
        conf_embed.set_footer(text=Help.version1)
        
        await ctx.send(embed=conf_embed)

        
    @commands.command(name="unban")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, userId):
        user = discord.Object(id=userId)
        await ctx.message.delete()
        await ctx.guild.unban(user)

        conf_embed = discord.Embed(title= "Réussi!", description="", color=discord.Color.green())
        conf_embed.set_author(name=f"Demandé par {ctx.author.name}", icon_url=ctx.author.avatar)
        conf_embed.add_field(name="Débanni:", value=f"<@{userId}> à été débanni du serveur par {ctx.author.mention}.", inline=False)
        conf_embed.set_footer(text=Help.version1)
    
        
        await ctx.send(embed=conf_embed)
        
    @commands.command(name='spam')
    @commands.has_permissions(administrator=True)
    async def spam(self, ctx, amount:int, *, message):
        await ctx.message.delete()
        max_amount = 15
        if amount > max_amount:
            await ctx.send(f"Le nombre maximum de messages que vous pouvez envoyer est de **{max_amount}**.")
            amount = max_amount
        sent_messages = 0
        while sent_messages < amount:
            if sent_messages >= max_amount:
                break
            await ctx.send(message)
            sent_messages += 1
            await asyncio.sleep(0.5) # Attendre une seconde entre chaque envoi de message
            

        
        
async def setup(client):
    await client.add_cog(Modo(client))