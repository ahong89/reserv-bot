from discord.ext import commands
from util import get_day
import manage_db as db
from api_calls import find_slots, make_booking, cancel_booking

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

    available_slots_msg = "Here's a list of 3 available slots that fit your requirements:\n\n"
    for i, s in enumerate(slots):
        available_slots_msg += f"Reservation #{i+1}: \n"
        available_slots_msg += f"Start: {s["start"]} \n"
        available_slots_msg += f"End: {s["end"]} \n"
        available_slots_msg += f"Duration: {s["duration"]}"
        available_slots_msg += "\n\n"
    available_slots_msg += "Respond with #<number reservation you want>"
    await ctx.send(available_slots_msg)
    user_data = db.get_user(ctx.author.id)

    def check(m):
        return m.author.id == ctx.author.id and m.channel == ctx.channel
    user_response = await driver_bot.wait_for('message', check=check)
    if user_response.content == "cancel":
        await ctx.send("Reserveration Canceled")
        return
    chosen_slot = int(user_response.content[1:]) - 1

    status_code, bookId = make_booking(user_data, slots[chosen_slot])
    if status_code == 200:
        await ctx.send("Reserveration Created! You should receieve an email shortly")
        db.add_booking(bookId, get_day(), slots[chosen_slot]["start"], slots[chosen_slot]["end"], ctx.author.id)
    else:
        await ctx.send("Reservation failed... something went wrong, error code: " + str(status_code))

@commands.hybrid_command(name="cancel")
async def cancel(ctx):
    if not db.user_exist(ctx.author.id):
        await ctx.send("Create an account first")
        return
    
    all_bookings = db.get_all_bookings(ctx.author.id)
    all_bookings_msg = "Here's a list of all your bookings: \n\n"
    for i, book in enumerate(all_bookings):
        all_bookings_msg += f"Booking #{i+1}\n"
        all_bookings_msg += "BookId: " + book[0] + "\n"
        all_bookings_msg += "Start Time: " + book[2] + "\n"
        all_bookings_msg += "End Time: " + book[3] + "\n"
    all_bookings_msg += "Repond with #<number booking you want to cancel>"
    await ctx.send(all_bookings_msg)

    def check(m):
        return m.author.id == ctx.author.id and m.channel == ctx.channel
    user_response = await driver_bot.wait_for('message', check=check)
    chosen_booking = int(user_response.content[1:]) - 1

    if cancel_booking(all_bookings[chosen_booking][0]):
        await ctx.send("Booking successfully canceled!")
    else:
        await ctx.send("Something went wrong :(")

command_list = [reserve, cancel]
driver_bot = None
async def setup(bot):
    global driver_bot
    for c in command_list:
        bot.add_command(c)
    driver_bot = bot