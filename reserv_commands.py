from discord.ext import commands
from datetime import datetime

import manage_db as db
from api_calls import find_slots

@commands.hybrid_command(name="reserve")
async def reserve(ctx, earliest_time=None, min_duration=None):
    if not db.user_exist(ctx.author.id):
        await ctx.send("Create an account first")
        return
    requirements = {
        "earliest-start": f"{getDay()} {earliest_time}",
        "min-duration": min_duration
    }
    print(requirements)
    slots = find_slots(requirements)
    await ctx.send(str(slots))
    # user_data = db.get_user(ctx.author.id)

    # await ctx.send("Reserveration Created! You should receieve an email shortly")

def getDay():
    return datetime.now().strftime("%Y-%m-%d")

command_list = [reserve]
driver_bot = None
async def setup(bot):
    global driver_bot
    for c in command_list:
        bot.add_command(c)
    driver_bot = bot