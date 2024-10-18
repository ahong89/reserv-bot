import discord
from discord.ext import commands

import os
import dotenv

import manage_db as db
import profile_commands
import reserv_commands

def get_token():
    dotenv.load_dotenv()
    return os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f' {bot.user} has logged on !')

    await bot.load_extension('profile_commands')
    await bot.load_extension('reserv_commands')

    await bot.tree.sync()

if __name__ == "__main__":
    bot.run(get_token())
    db.close_connection()