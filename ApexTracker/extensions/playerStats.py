from logging import exception
from urllib.error import HTTPError
import hikari
import lightbulb
from lightbulb import commands
import requests
import json
import datetime as dt
import os

plugin = lightbulb.Plugin("PlayerStats")


# json load
with open("./ApexTracker/images/emojis.json") as f:
    emoji_data = json.load(f)

@plugin.command()
@lightbulb.option(name="username", description="For PC players you must use origin account name.")
@lightbulb.option(
    name="platform", description="The platform the player is playing on.",
    choices=("PC (Steam or Origin)", "PS4 or PS5", "Xbox"),)
@lightbulb.command("player_stats", "Shows player statistics using the player's username")
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def cmd_rotation(ctx) -> None:

    #  user selected options
    username = ctx.options['username']
    platform = ctx.options['platform']
    if platform == "PC (Steam or Origin)": platform = "PC"
    elif platform == "PS4 or PS5": platform = "PS4"
    elif platform == "Xbox": platform = "X1"

    # API call
    
    try:
        url = requests.get(f"https://api.mozambiquehe.re/bridge?auth={os.environ['API_KEY_ID']}&player={username}&platform={platform}")
    except requests.exceptions.RequestException as e:
        await ctx.send("API call error.")
        return
    
    data = json.loads(url.text)

    # Errors exists
    if "Error" in data:
        await ctx.respond(f"Player not found. Try again?")
        return
        
    stats = basicPlayerStats(data)

    #Embed
    embed = (
        hikari.Embed(
            title=f"Stats for {stats['name']}",
            description="",
            color="#674ea7",
            timestamp=dt.datetime.now().astimezone()
        )
        # .set_thumbnail(stats['selectedLegendImgIcon'])
        .set_image(stats['selectedLegendImgBanner'])
        .set_footer(
            f"name: {stats['name']} · uid: {stats['uid']} · Status: {stats['status']}\n"
            f"Requested by {ctx.member.display_name}",
            icon=ctx.member.display_avatar_url
        )
        # .add_field(
        #     name="Status",
        #     value=f"{stats['status']}",
        #     inline=False
        # )
        .add_field(
            name="Total Kills᲼᲼",
            value=f"{stats['totalKills']}",
            inline=True
        )
        .add_field(
            name="Total Damage᲼᲼",
            value=f"{stats['totalDmg']}",
            inline=True
        )
        .add_field(
            name="K/D",
            value=f"{stats['kd']}",
            inline=True
        )
        .add_field(
            name="Level",
            value=f"{emoji_data['Account']['Level']} {stats['level']}\n\n"
            "**BR Rank**\n"
            f"{emoji_data['Ranked'][stats['br_rankName']]} {stats['br_rankName']} {stats['br_rankDivision']} \n"
            f"--> {stats['br_rankScore']} RP",
            inline=True
        )
        .add_field(
            name="Battle Pass",
            value=f"{emoji_data['Account']['BattlePass']} {stats['bp_level']}\n\n"
            "**Arenas Rank**\n"
            f"{emoji_data['Ranked'][stats['arena_rankName']]} {stats['arena_rankName']} {stats['arena_rankDivision']} \n"
            f"--> {stats['arena_rankScore']} AP",
            inline=True
        )
        .add_field(
            name="\u200b",
            value="**Trackers Equipped**",
            inline=False
        )
    )
    if stats['numTrackers'] == 0:
        embed.add_field(name=f"_", value=f"_", inline=True)
        embed.add_field(name=f"_", value=f"_", inline=True)
        embed.add_field(name=f"_", value=f"_", inline=True)
    elif stats['numTrackers'] == 1:
        embed.add_field(name=f"{stats['tracker_1_name']}", value=f"{stats['tracker_1_value']}", inline=True)
        embed.add_field(name=f"_", value=f"_", inline=True)
        embed.add_field(name=f"_", value=f"_", inline=True)
    elif stats['numTrackers'] == 2:
        embed.add_field(name=f"{stats['tracker_1_name']}", value=f"{stats['tracker_1_value']}", inline=True)
        embed.add_field(name=f"{stats['tracker_2_name']}", value=f"{stats['tracker_2_value']}", inline=True)
        embed.add_field(name=f"_", value=f"_", inline=True)
    elif stats['numTrackers'] == 3:
        embed.add_field(name=f"{stats['tracker_1_name']}", value=f"{stats['tracker_1_value']}", inline=True)
        embed.add_field(name=f"{stats['tracker_2_name']}", value=f"{stats['tracker_2_value']}", inline=True)
        embed.add_field(name=f"{stats['tracker_3_name']}", value=f"{stats['tracker_3_value']}", inline=True)


    # Response
    await ctx.respond(embed)

def basicPlayerStats(data: dict) -> dict:
    res = {}

    # General info
    res['name'] = data['global']['name']
    res['uid'] = data['global']['uid']
    res['level'] = data['global']['level']

    if res['level'] == "-1": res['level'] = "0"

    res['bp_level'] = data['global']['battlepass']['level']

    if res['bp_level'] == "-1": res['bp_level'] = "0"

    res['selectedLegendImgIcon'] = data['legends']['selected']['ImgAssets']['icon']
    res['selectedLegendImgBanner'] = data['legends']['selected']['ImgAssets']['banner']

    # Status
    res['status'] = data['realtime']['currentStateAsText']

    # BR Rank Info
    res['br_rankName'] = data['global']['rank']['rankName']
    res['br_rankScore'] = data['global']['rank']['rankScore']
    res['br_rankDivision'] = data['global']['rank']['rankDiv']
    res['br_laddPos'] = data['global']['rank']['ladderPosPlatform']
    
    if res['br_rankName'] == "Apex Predator": res['br_rankDivision'] = f"**[#{res['br_laddPos']}]**"

    res['br_rankImage'] = data['global']['rank']['rankImg']
    res['br_rankedSeason'] = data['global']['rank']['rankedSeason']

    # Arenas Rank Info
    res['arena_rankName'] = data['global']['arena']['rankName']
    res['arena_rankScore'] = data['global']['arena']['rankScore']
    res['arena_rankDivision'] = data['global']['arena']['rankDiv']
    res['arena_laddPos'] = data['global']['arena']['ladderPosPlatform']

    if res['arena_rankName'] == "Apex Predator": res['arena_rankDivision'] = f"**[#{res['arena_laddPos']}]**"

    res['arena_rankImage'] = data['global']['arena']['rankImg']
    res['arena_rankedSeason'] = data['global']['arena']['rankedSeason']
    
    # KILLS
    if "kills" in data['total']: 
        if data['total']['kills']['value'] == "-1": res['totalKills'] = "_"
        else: res['totalKills'] = data['total']['kills']['value']
    else: res['totalKills'] = "_"

    # DAMAGE
    if "damage" in data['total']: 
        if data['total']['damage']['value'] == "-1": res['totalDamage'] = "_"
        else: res['totalDmg'] = data['total']['damage']['value']
    else: res['totalDmg'] = "_"

    # KD
    if "kd" in data['total']: 
        if data['total']['kd']['value'] == "-1": res['kd'] = "_"
        else:res['kd'] = data['total']['kd']['value']
    else: res['kd'] = "_"

    # Trackers
    trackers = data['legends']['selected']['data']
    counter = 0
    for tracker in trackers:
        if counter == 3:
            break
        # print(tracker)
        res[f'tracker_{str(counter+1)}_name'] = data['legends']['selected']['data'][counter]['name']
        res[f'tracker_{str(counter+1)}_value'] = data['legends']['selected']['data'][counter]['value']
        counter += 1

    res['numTrackers'] = counter
    return res

def load(bot) -> None:
    bot.add_plugin(plugin)

def unload(bot) -> None:
    bot.remove_plugin(plugin)