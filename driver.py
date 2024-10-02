import discord
from discord.ext import commands
from typing import Optional

import requests
import os
import dotenv

import api_calls
import manage_db as db

def get_token():
    dotenv.load_dotenv()
    return os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

import profile_commands

@bot.event
async def on_ready():
    print(f' {bot.user} has logged on !')

    await bot.load_extension('profile_commands')
    
    await bot.tree.sync()

if __name__ == "__main__":
    bot.run(get_token())
    db.close_connection()