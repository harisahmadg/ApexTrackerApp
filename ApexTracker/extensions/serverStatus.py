from logging import exception
from urllib.error import HTTPError
import hikari
import lightbulb
from lightbulb import commands
import requests
import json
import datetime as dt
import os

plugin = lightbulb.Plugin("ServerStatus")


# json load
with open("./ApexTracker/images/emojis.json") as f:
    emoji_data = json.load(f)

@plugin.command()
@lightbulb.command("server_status", "Shows the current server status.")
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def cmd_rotation(ctx) -> None:

    # API call
    
    try:
        url = requests.get(f"https://api.mozambiquehe.re/servers?auth={os.environ['API_KEY_ID']}")
    except requests.exceptions.RequestException as e:
        await ctx.send("API call error.")
        return
    
    data = json.loads(url.text)

    # Errors exists
    if "Error" in data:
        await ctx.respond(f"Player not found. Try again?")
        return
    
    # Data parsing

    #Embed
    embed = (
        hikari.Embed(
            title=f"Server Status",
            description="",
            color="#674ea7",
            timestamp=dt.datetime.now().astimezone()
        )
        .set_footer(
            f"Requested by {ctx.member.display_name}",
            icon=ctx.member.display_avatar_url
        )
        # .set_image('ApexTracker/images/Apex_Servers.jpg')
    )

    # Server Type
    embed.add_field(
    name=f"\u200b",
    value=f"**Origin & Steam**",
    inline=False
    )

    for region in data['Origin_login']:
        server_status = data['Origin_login'][region]['Status']
        if server_status == 'UP':
            embed.add_field(
            name=f"{region}",
            value=f"{emoji_data['serverStatus']['other']['Green']} {data['Origin_login'][region]['ResponseTime']} ms",
            inline=True
            )
        elif server_status =='SLOW':
            embed.add_field(
            name=f"{region}",
            value=f"{emoji_data['serverStatus']['other']['Yellow']} {data['Origin_login'][region]['ResponseTime']} ms",
            inline=True
            )
        else:
            embed.add_field(
            name=f"{region}",
            value=f"{emoji_data['serverStatus']['other']['Red']} {data['Origin_login'][region]['ResponseTime']} ms",
            inline=True
            )

    # Server Type
    embed.add_field(
    name=f"\u200b",
    value=f"**EA Accounts**",
    inline=False
    )

    for region in data['EA_accounts']:
        server_status = data['EA_accounts'][region]['Status']
        if server_status == 'UP':
            embed.add_field(
            name=f"{region}",
            value=f"{emoji_data['serverStatus']['other']['Green']} {data['EA_accounts'][region]['ResponseTime']} ms",
            inline=True
            )
        elif server_status =='SLOW':
            embed.add_field(
            name=f"{region}",
            value=f"{emoji_data['serverStatus']['other']['Yellow']} {data['EA_accounts'][region]['ResponseTime']} ms",
            inline=True
            )
        else:
            embed.add_field(
            name=f"{region}",
            value=f"{emoji_data['serverStatus']['other']['Red']} {data['EA_accounts'][region]['ResponseTime']} ms",
            inline=True
            )

    # Server Type
    embed.add_field(
    name=f"\u200b",
    value=f"**Cross Play**",
    inline=False
    )

    for region in data['ApexOauth_Crossplay']:
        server_status = data['ApexOauth_Crossplay'][region]['Status']
        if server_status == 'UP':
            embed.add_field(
            name=f"{region}",
            value=f"{emoji_data['serverStatus']['other']['Green']} {data['ApexOauth_Crossplay'][region]['ResponseTime']} ms",
            inline=True
            )
        elif server_status =='SLOW':
            embed.add_field(
            name=f"{region}",
            value=f"{emoji_data['serverStatus']['other']['Yellow']} {data['ApexOauth_Crossplay'][region]['ResponseTime']} ms",
            inline=True
            )
        else:
            embed.add_field(
            name=f"{region}",
            value=f"{emoji_data['serverStatus']['other']['Red']} {data['ApexOauth_Crossplay'][region]['ResponseTime']} ms",
            inline=True
            )

    # Response
    await ctx.respond(embed)


def load(bot) -> None:
    bot.add_plugin(plugin)

def unload(bot) -> None:
    bot.remove_plugin(plugin)