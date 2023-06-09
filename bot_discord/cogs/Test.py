import discord
from discord.ext import commands
import openai

class Test(commands.Cog):
    def __init__(self, client):
        self.client = client
        with open("C:/Users/danie/Mon Drive/tokengpt.txt", "r") as f:
            GPT_API_KEY = f.read().strip()
        openai.api_key = GPT_API_KEY

        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Test.py is ready")

    @commands.command()
    async def gpt(self, ctx, *, question):
        async with ctx.typing():
            response = self.generer_reponse(question)
            response = self.nettoyer_texte(response)
        await ctx.send(response)

    def generer_reponse(self, question):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=question,
            max_tokens=200,
            n=1,
            stop=None,
            temperature=0.9
        )
        bot_response = response.choices[0].text.strip()
        return bot_response

    def nettoyer_texte(self, texte):
        # Supprimer les sauts de ligne redondants
        texte_nettoye = "\n".join(line for line in texte.splitlines() if line.strip())
        return texte_nettoye
    
async def setup(client):
    await client.add_cog(Test(client))
