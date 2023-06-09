import discord 
from discord import Activity, ActivityType, app_commands
from discord.ext import commands, tasks
from itertools import cycle
import os
import asyncio
from cogs import Help
import io
import traceback



client = commands.Bot(command_prefix="=", intents= discord.Intents.all())

activities = cycle([
    Activity(name='Crococlip 🐊', type=discord.ActivityType.playing),
    Activity(name='Geogebra Mode Examen 📊', type=discord.ActivityType.playing),
    Activity(name='Coding 👨‍💻', type=ActivityType.listening),
    Activity(name='MBN Modding 🔧', type=ActivityType.streaming, url='https://www.youtube.com/watch?v=nPeqfo4kkGw'),
    Activity(name='Samsung Watch 5 Pro ⌚', type=discord.ActivityType.playing),
])


@client.event
async def on_message(message):
    if client.user.mentioned_in(message):  # Vérifie si le bot est mentionné dans le message
        async with message.channel.typing():
            await asyncio.sleep(1)  # Simulation de l'écriture du bot (1 secondes dans cet exemple)
            await message.channel.send(f"Oh salut {message.author.mention}, fais ``=helps`` pour connaitre les différentes commandes.")
    else:
        await client.process_commands(message)


@client.event
async def on_ready():
    await asyncio.sleep(1)
    print("main.py is ready")
    print("")
    change_activity.start()
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} slash commands")
        print("Everything loaded up Bot Ready!")
    except Exception as e:
        print(e)
        
@client.tree.command(name="ping", description="show ping in ms")
async def ping(interaction: discord.Interaction):
    bot_latency = round(client.latency * 1000)
    await interaction.response.send_message(f"Pong! {bot_latency} ms.")


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")


@tasks.loop(seconds=7)
async def change_activity():
    activity = next(activities)
    await client.change_presence(activity=activity)
   
# show if commands exist
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title= "Commande inconnue", description="Utilisez **=helps** pour la liste des commandes", color=discord.Color.red())
        embed.set_image(url=ctx.guild.icon)
        embed.set_footer(text=Help.version1)
        await ctx.send(embed=embed, delete_after=10)       

# stop the bot
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
    with open("C:/Users/danie/Mon Drive/token.txt", "r") as f:
        token = f.read().strip()
    client.run(token)

except Exception as e:
    print("Arrêté impossible de lancer le bot")
    traceback.print_exc()