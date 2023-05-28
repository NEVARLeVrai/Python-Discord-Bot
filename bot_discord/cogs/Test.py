import discord
from discord.ext import commands
from dotenv import load_dotenv
from cogs import Help
from datetime import datetime
import traceback
import pytz

class Test(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Test.py is ready")

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
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to manage messages.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter the name of the channel to delete.")
        else:
            await ctx.send("An error occurred while processing the command.")

    
    @cleanraidmultiple.error
    async def cleanraidmultiple_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to manage messages.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please enter a valid raid date and time in the format 'YYYY-MM-DD HH:MM'.")
        else:
            await ctx.send("An error occurred while processing the command.")



async def setup(client):
    await client.add_cog(Test(client))