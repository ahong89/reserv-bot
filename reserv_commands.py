from discord.ext import commands
from util import get_day, get_earliest_time
import manage_db as db
from api_calls import find_slots, make_booking, cancel_booking

@commands.hybrid_command(name="reserve")
async def reserve(ctx, earliest_time=None, time_offset=None, min_duration="01:00:00", day="UNASSIGNED"):
    if not db.user_exist(ctx.author.id):
        await ctx.send("Create an account first")
        return
    
    #parsing earliest_time and time_offset
    if not earliest_time and not time_offset:
        if(day != get_day()):
            earliest_time = '00:00:00'
        else:
            earliest_time = get_earliest_time()
    elif not earliest_time and time_offset:
        hour_offset, min_offset = None
        if time_offset.contains(':'):
            hour_offset = time_offset.split(':')[0]
            min_offset = int(time_offset.split(':')[1])
        else:
            hour_offset = int(time_offset)
            min_offset = 0
        earliest_time = get_earliest_time(hour_offset, min_offset)
    elif earliest_time and time_offset:
        await ctx.send('Have both time_offset or earliest_time, pick one, ending command')
        return
    
    if earliest_time.count(':') == 1:
        earliest_time += ":00"
    temp_time = ''
    for time_value in earliest_time.split(':'):
        temp_time += (time_value if len(time_value) == 2 else '0' + time_value) + ':'
    earliest_time = temp_time[:-1]

    if min_duration.count(':') == 1:
        min_duration += ":00"
    elif min_duration.count(':') == 0:
        min_duration += ":00:00"
    temp_duration = ''
    for time_value in min_duration.split(':'):
        temp_duration += (time_value if len(time_value) == 2 else '0' + time_value) + ':'
    min_duration = temp_duration[:-1]

    if day == "UNASSIGNED":
        day = get_day()
    elif day.count('-') != 2:
        await ctx.send('Incorrect formatting for day. Use YYYY-MM-DD')
        return

    requirements = {
        "earliest-start": f"{day} {earliest_time}",
        "min-duration": min_duration
    }
    # print(requirements)
    slots = find_slots(requirements)
    if len(slots) == 0:
        await ctx.send('No slots are available right now with those constraints, check back later')
        return

    available_slots_msg = f"Here's a list of {len(slots)} available slots that fit your requirements:\n\n"
    for i, s in enumerate(slots):
        available_slots_msg += f"Reservation #{i+1}: \n"
        available_slots_msg += f"Start: {s['start']} \n"
        available_slots_msg += f"End: {s['end']} \n"
        available_slots_msg += f"Duration: {s['duration']}"
        available_slots_msg += "\n\n"
    available_slots_msg += "Respond with #<number reservation you want> (or \"stop\" to cancel)"
    await ctx.send(available_slots_msg)
    user_data = db.get_user(ctx.author.id)

    def check(m):
        return m.author.id == ctx.author.id and m.channel == ctx.channel
    user_response = await driver_bot.wait_for('message', check=check)
    if user_response.content[:1] != "#":
        await ctx.send("Reserveration Canceled, respond with the correct format")
        return
    chosen_slot = int(user_response.content[1:]) - 1

    status_code, bookId = make_booking(user_data, slots[chosen_slot])
    if status_code == 200:
        await ctx.send("Reserveration Created! You should receieve an email shortly")
        db.add_booking(bookId, get_day(), slots[chosen_slot]["start"], slots[chosen_slot]["end"], ctx.author.id)
    else:
        await ctx.send("Reservation failed... something went wrong, error: " + str(status_code) + " " + bookId)

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
    all_bookings_msg += "Repond with #<number booking you want to cancel> (or \"stop\" to stop)"
    await ctx.send(all_bookings_msg)

    def check(m):
        return m.author.id == ctx.author.id and m.channel == ctx.channel
    user_response = await driver_bot.wait_for('message', check=check)
    if user_response.content == "stop":
        await ctx.send("Cancellation stopped")
        return
    chosen_booking = int(user_response.content[1:]) - 1
    if cancel_booking(all_bookings[chosen_booking][0]):
        db.delete_booking(all_bookings[chosen_booking][0])
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
