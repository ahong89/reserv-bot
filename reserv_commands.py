from discord.ext import commands
from util import get_day
import manage_db as db
from api_calls import find_slots, make_booking

@commands.hybrid_command(name="reserve")
async def reserve(ctx, earliest_time=None, min_duration=None):
    if not db.user_exist(ctx.author.id):
        await ctx.send("Create an account first")
        return
    requirements = {
        "earliest-start": f"{get_day()} {earliest_time}",
        "min-duration": min_duration
    }
    slots = find_slots(requirements)
    print(slots)

    available_slots_msg = "Here's a list of 3 available slots that fit your requirements:\n\n"
    for i, s in enumerate(slots):
        available_slots_msg += f"Reservation #{i+1}: \n"
        available_slots_msg += f"Start: {s["start"]} \n"
        available_slots_msg += f"End: {s["end"]} \n"
        available_slots_msg += f"Duration: {s["duration"]}"
        available_slots_msg += "\n\n"
    available_slots_msg += "Response with #<number reservation you want>"
    await ctx.send(available_slots_msg)
    user_data = db.get_user(ctx.author.id)
    print(user_data)

    def check(m):
        return m.author.id == ctx.author.id and m.channel == ctx.channel
    user_response = await driver_bot.wait_for('message', check=check)
    if user_response.content == "cancel":
        await ctx.send("Reserveration Canceled")
        return
    chosen_slot = int(user_response.content[1:]) - 1

    status_code = make_booking(user_data, slots[chosen_slot])
    if status_code == 200:
        await ctx.send("Reserveration Created! You should receieve an email shortly")
    else:
        await ctx.send("Reservation failed... something went wrong, error code: " + str(status_code))

command_list = [reserve]
driver_bot = None
async def setup(bot):
    global driver_bot
    for c in command_list:
        bot.add_command(c)
    driver_bot = bot