import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

class Test(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Test.py is ready")

    @commands.command(aliases=["clrs"])
    async def cleanraidsimple(self, ctx, name):
        found = False
        channeldel = None
        
        for channel in self.client.get_all_channels():
            if channel.name == name:
                found = True
                channeldel = channel
                
        if found:
            await ctx.send(f"Salon **{channel}** suppr")
            await channeldel.delete()
            await ctx.send("Salon supprimé.")
    
        else:
            await ctx.send(f"Aucun salon avec le nom **{name}** trouvé.")

async def setup(client):
    await client.add_cog(Test(client))