import hikari
import lightbulb
from lightbulb import commands
import requests
import json
import datetime as dt
import os

plugin = lightbulb.Plugin("Rotation")


# json load
with open("./ApexTracker/images/emojis.json") as f:
    emoji_data = json.load(f)

@plugin.command()
@lightbulb.option(
    name="map", description="Selects the map to display its rotation.", 
    choices=("arenas", "arenas ranked", "battle royale", "battle royale ranked", "control"),
    default="Batte Royale")
@lightbulb.command("rotation", "Shows the rotation of the selected map (default=Battle Royale)")
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def cmd_rotation(ctx) -> None:

    #  user selected options
    map = ctx.options['map']

    # API call
    url = requests.get(f"https://api.mozambiquehe.re/maprotation?auth={os.environ['API_KEY_ID']}&version=2")
    data = json.loads(url.text)

    # Errors exists
    if "Error" in data:
        await ctx.respond("Please select a valid map.")
        return

    res = basicMapInformation(data, map)

    #Embed
    embed = (
        hikari.Embed(
            title=f"{map}: {res['curr_map']}",
            description=res['description_1'] + res['description_2'],
            color="#674ea7",
            timestamp=dt.datetime.now().astimezone()
        )
        .set_image(res['image'])
        # .set_thumbnail("TheApexTracker/images/wraith.jpg")    add logo
        .set_footer(
            f"Requested by {ctx.member.display_name}",
            icon=ctx.member.display_avatar_url
        )
    )

    # Response
    await ctx.respond(embed)


def basicMapInformation(data: dict, map: str) -> dict:
    res = {}
    map = map.lower()
    if map == "arenas": pass # already correct form
    elif map =="arenas ranked": map="arenasRanked"
    elif map =="battle royale": map="battle_royale"
    elif map =="battle royale ranked": map="ranked"
    elif map == "control": pass # already correct form

    # Data
    res['image'] = data[map]['current']['asset']
    curr_map = data[map]['current']['map']
    res['curr_map'] = curr_map
    next_map = data[map]['next']['map']

    # time 
    curr_secs = data[map]['current']['remainingSecs']
    curr_mins = curr_secs // 60
    curr_default_mins = curr_mins
    curr_hours = curr_mins // 60
    curr_days = curr_hours // 24
    
    next_secs = data[map]['next']['DurationInSecs']
    next_mins = next_secs // 60
    next_default_mins = next_mins
    next_hours = next_mins // 60
    next_days = next_hours // 24
    
    # Mod
    curr_secs %= 60
    curr_mins %= 60
    curr_hours %= 24
    curr_days %= 365
    next_secs %= 60
    next_mins %= 60
    next_hours %= 24
    next_days %= 365

    # Edit current time left description
    if curr_default_mins < 60: # use mins and seconds
        res['description_1'] = f"{curr_map} ends in {curr_mins} minutes and {curr_secs} seconds.\n"

    elif curr_default_mins < 144:  # use hours mins
        res['description_1'] = f"{curr_map} ends in {curr_hours} hours and {curr_mins} minutes.\n"

    else: # use days also
        res['description_1'] = f"{curr_map} ends in {curr_days} days and {curr_hours} hours.\n"

    
    # Edit next map time left description
    if next_default_mins < 60: # use mins and seconds
        res['description_2'] = f"**Next:** {next_map} for {next_mins} minutes and {next_secs} seconds."

    elif next_default_mins < 144:  # use hours mins
        res['description_2'] = f"**Next:** {next_map} for {next_hours} hours and {next_mins} minutes."

    else: # use days also
        res['description_2'] = f"**Next:** {next_map} for {next_days} days and {next_hours} hours."
    
    # if next is unknown then description_2 will be empty.
    if next_map == 'Unknown':
        res['description_2'] = ""

    return res

def load(bot) -> None:
    bot.add_plugin(plugin)

def unload(bot) -> None:
    bot.remove_plugin(plugin)