import discord
from discord.ext import commands

import requests
import os
import dotenv

import api_calls

def get_token():
    dotenv.load_dotenv()
    return os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.hybrid_command()
async def res(ctx):
    await ctx.send("shut up")

@bot.event
async def on_ready():
    print(f' {bot.user} has logged on !')
    await bot.tree.sync()

if __name__ == "__main__":
    bot.run(get_token())