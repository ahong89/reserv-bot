from discord.ext import commands

import manage_db as db

@commands.hybrid_command(name="createprofile")
async def create_profile(ctx, fname=None, lname=None, email=None, school_uid=None):
    if db.user_exist(ctx.author.id):
        await ctx.send("Account already exists")
        return
    if fname is None:
        fname = await query_user(ctx, "first name")
    if lname is None:
        lname = await query_user(ctx, "last name")
    if email is None:
        email = await query_user(ctx, "email")
    if school_uid is None:
        school_uid = await query_user(ctx, "school uid")

    db.create_profile(ctx.author.id, fname, lname, school_uid, email)
    await ctx.send("Profile Created!")

@commands.hybrid_command(name="updateprofile")
async def update_profile(ctx, attr=None, new_value=None):
    if attr is None:
        attr = await query_user(ctx, "attribute")
    if new_value is None:
        new_value = await query_user(ctx, "new value")
    db.update_profile(ctx.author.id, attr, new_value)
    await ctx.send("User profile updated")

@commands.hybrid_command(name="deleteprofile")
async def delete_profile(ctx):
    if not db.user_exist(ctx.author.id):
        await ctx.send("Account doesn't exist yet")
        return
    db.delete_profile(ctx.author.id)
    await ctx.send(f"{ctx.author.name}'s profile deleted!")

@commands.hybrid_command(name="viewprofile")
async def view_profile(ctx):
    if not db.user_exist(ctx.author.id):
        await ctx.send("Account doesn't exist")
        return
    user_data = db.get_user(ctx.author.id)
    await ctx.send(str(user_data))

async def query_user(ctx, attribute):
    await ctx.send(f"Enter your {attribute}")
    def check(m):
        return m.author.id == ctx.author.id and m.channel == ctx.channel
    output = await driver_bot.wait_for('message', check=check)
    return output.content

command_list = [create_profile, update_profile, delete_profile, view_profile]
driver_bot = None
async def setup(bot):
    global driver_bot
    for c in command_list:
        bot.add_command(c)
    driver_bot = bot
