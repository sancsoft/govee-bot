import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import requests
from datetime import datetime

# Load token from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Define Intents
intents = discord.Intents.default()
intents.message_content = True

# Setup Bot
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.name}!')

@bot.command()
async def temperature(ctx):
    await temp(ctx)

@bot.command()
async def temp(ctx):
    response = requests.get("http://192.168.5.154/api/sensor")
    data = response.json()
    temperature = data.get("temp")
    count = data.get("cnt")
    tempf = temperature * 9 / 5 + 32.0
    message = ""
    if (tempf >= 69.0 and tempf < 70.0):
        message = "Nice"
    elif (tempf >= 67.0 and tempf <= 75.0):
        message = "Reasonable"
    elif (tempf < 67.0):
        message = "It's getting chilly in here"
    elif (tempf > 75.0 and tempf < 80):
        message = "C'mon man, its hot"
    elif (tempf >= 80):
        message = "This is fine ...."
    now = datetime.now()

    await ctx.send(f'Office Temperature = {tempf:.1f}F on {now.strftime("%Y-%m-%d at %H:%M:%S")} - {message} - Update #{count}')

bot.run(TOKEN)
