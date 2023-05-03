import discord
from discord import Activity, ActivityType
from discord.ext import commands, tasks
from itertools import cycle
import os
import asyncio
from cogs import Help
import io
import traceback

client = commands.Bot(command_prefix="=", intents=discord.Intents.all())
activities = cycle([
    Activity(name='Crococlip', type=discord.ActivityType.playing),
    Activity(name='Geogebra Mode Examen', type=discord.ActivityType.playing),
    Activity(name='Coding', type=ActivityType.listening),
    Activity(name='MBN Modding', type=ActivityType.streaming, url='https://www.youtube.com/watch?v=nPeqfo4kkGw'),
    Activity(name='Samsung Watch 5 Pro', type=discord.ActivityType.playing),
])




    
@tasks.loop(seconds=7)
async def change_activity():
    activity = next(activities)
    await client.change_presence(activity=activity)


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")


# ping in / command

@client.tree.command(name="ping", description="show ping in ms test")
async def ping(interaction: discord.Interaction):
        bot_latency = round(client.latency * 1000)
        await interaction.response.send_message(f"Pong! {bot_latency} ms.")
        
@client.event
async def on_ready():
    await asyncio.sleep(1)
    print("")
    print("Bot Ready!")
    change_activity.start()

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title= "Commande inconnue", description="Utilisez **=help** pour la liste des commandes", color=discord.Color.red())
        embed.set_image(url=ctx.guild.icon)
        embed.set_footer(text=Help.version1)
        await ctx.send(embed=embed, delete_after=10)

  


@client.command()
@commands.is_owner()
async def stop(ctx):
    await ctx.message.delete()
    bot_latency = round(client.latency * 1000)
    embed = discord.Embed(title= "Arrêt", description=f"Le Bot s'arrête Ping {bot_latency} ms.", color=discord.Color.red())
    embed.set_footer(text=Help.version1)
    with open("./Autres/hilaire2.png", "rb") as f:
        image_data = f.read()
    embed.set_thumbnail(url="attachment://hilaire2.png")
    embed.set_image(url=ctx.guild.icon)
    await ctx.send(embed=embed, file=discord.File(io.BytesIO(image_data), "hilaire2.png"))
    print("")
    print("Arrêté par l'utilisateur")
    print("")
    await client.close()


# Run the bot
try:
    asyncio.run(load())
    print("")
    with open("C:/Users/danie/Documents/VSC/Bot_Discord_Folder/token.txt", "r") as f:
        token = f.read().strip()
    client.run(token)

except Exception as e:
    print("Arrêté impossible de lancer le bot")
    traceback.print_exc()