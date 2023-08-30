import discord
from discord.ext import commands
import asyncio
from cogs import Help
import traceback
from dotenv import load_dotenv
from datetime import datetime
import pytz
import requests


class Mods(commands.Cog):
    def __init__(self, client):
        self.client = client    



    @commands.Cog.listener()
    async def on_ready(self):
        print("Mods.py is ready")


        
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
        max_amount = 200
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
            
    @commands.command(aliases=["clr"])
    @commands.has_permissions(manage_messages=True)
    async def cleanraidsimple(self, ctx, name):
        found = False
        channeldel = None 
        
        for channel in self.client.get_all_channels():
            if channel.name == name:
                found = True
                channeldel = channel
                        
        if found:
            embed4 = discord.Embed(title="Nettoyage Raid par nom", description=f"Suppression des ou d'un Salon(s) **{channel}**", color=discord.Color.yellow())
            embed4.set_author(name=f"Demandé par {ctx.author.name}", icon_url=ctx.author.avatar)
            embed4.set_footer(text=Help.version1)
            await ctx.send(embed=embed4, delete_after=5)           
            await channeldel.delete()
            embed3 = discord.Embed(title="Nettoyage Raid par nom", description=f"Salon(s) **{channel}** supprimé avec succès!", color=discord.Color.green())
            embed3.set_author(name=f"Demandé par {ctx.author.name}", icon_url=ctx.author.avatar)
            embed3.set_footer(text=Help.version1)
            await ctx.send(embed=embed3, delete_after=5)
            
        else:
            embed5 = discord.Embed(title="Nettoyage Raid par nom", description=f"Aucun Salon(s) avec le nom **{name}** trouvé.", color=discord.Color.red())
            embed5.set_author(name=f"Demandé par {ctx.author.name}", icon_url=ctx.author.avatar)
            embed5.set_footer(text=Help.version1)
            await ctx.send(embed=embed5, delete_after=5)

    @commands.command(aliases=["clrs"])
    @commands.has_permissions(manage_messages=True)
    async def cleanraidmultiple(self, ctx, raid_date: str, raid_time: str):
        raid_datetime_str = raid_date + " " + raid_time.replace("h", ":")
        raid_datetime = datetime.strptime(raid_datetime_str, "%Y-%m-%d %H:%M")
        time_difference = datetime.now(pytz.utc).hour - datetime.now().hour
        raid_datetime = raid_datetime.replace(hour=time_difference+raid_datetime.hour, tzinfo=pytz.UTC)
        for channel in self.client.get_all_channels():
            if channel.created_at > raid_datetime:
                await channel.delete()
        embed6 = discord.Embed(title="Nettoyage Raid par temps", description=f"Salon(s) entre **{raid_datetime}** ont été supprimés", color=discord.Color.green())
        embed6.set_author(name=f"Demandé par {ctx.author.name}", icon_url=ctx.author.avatar)
        embed6.set_footer(text=Help.version1)
        await ctx.send(embed=embed6, delete_after=5)

    @cleanraidsimple.error
    async def cleanraidsimple_error(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to manage messages.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter the name of the channel to delete.")
        else:
            await ctx.send("An error occurred while processing the command.")

    
    @cleanraidmultiple.error
    async def cleanraidmultiple_error(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to manage messages.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please enter a valid raid date and time in the format 'YYYY-MM-DD HH:MM'.")
        else:
            await ctx.send("An error occurred while processing the command.")
                  
async def setup(client):
    await client.add_cog(Mods(client))