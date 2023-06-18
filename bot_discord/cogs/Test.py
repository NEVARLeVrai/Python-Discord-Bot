import discord
from discord.ext import commands
import requests


class Test(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Test.py is ready")



async def setup(client):
    await client.add_cog(Test(client))
