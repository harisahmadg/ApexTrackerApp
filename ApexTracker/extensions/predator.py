import hikari
import lightbulb
from lightbulb import commands
import requests
import json
import datetime as dt
import os

plugin = lightbulb.Plugin("Predator")

# json load
with open("./ApexTracker/images/emojis.json") as f:
    emoji_data = json.load(f)


@plugin.command()
@lightbulb.command("predator", "Shows the RP/AP needed to reach Apex Predator on each platform.)")
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def cmd_predator(ctx) -> None:

    # API call
    url = requests.get(f"https://api.mozambiquehe.re/predator?auth={os.environ['API_KEY_ID']}")
    data = json.loads(url.text)
    
    # Error exists
    if "Error" in data:
        await ctx.respond("Error: " + data['Error'])
        return

    #Embed
    embed = (
        hikari.Embed(
            title="RP/AP needed to reach Apex Predator",
            description=f"There's a total of {data['RP']['PC']['totalMastersAndPreds']} masters and predators in battle royale PC.",
            color="#674ea7",
            timestamp=dt.datetime.now().astimezone()
        )
        .add_field(
            name="Battle Royale",
            value=(
                f"{emoji_data['platform']['PC']} PC: {'{:,}'.format(data['RP']['PC']['val'])} RP | {data['RP']['PC']['totalMastersAndPreds']} Players ᲼᲼᲼\n"
                f"{emoji_data['platform']['PS4']} PS4: {'{:,}'.format(data['RP']['PS4']['val'])} RP | {data['RP']['PS4']['totalMastersAndPreds']} Players᲼᲼᲼\n"
                f"{emoji_data['platform']['Xbox']} Xbox: {'{:,}'.format(data['RP']['X1']['val'])} RP | {data['RP']['X1']['totalMastersAndPreds']} Players᲼᲼᲼\n"
                f"{emoji_data['platform']['Switch']} Switch: {'{:,}'.format(data['RP']['SWITCH']['val'])} RP | {data['RP']['SWITCH']['totalMastersAndPreds']} Players᲼᲼᲼\n"
            ),
            inline=True
        )
        .add_field(
            name="Arenas",
            value=(
                f"{emoji_data['platform']['PC']} PC: {'{:,}'.format(data['AP']['PC']['val'])} RP | {data['AP']['PC']['totalMastersAndPreds']} Players\n"
                f"{emoji_data['platform']['PS4']} PS4: {'{:,}'.format(data['AP']['PS4']['val'])} RP | {data['AP']['PS4']['totalMastersAndPreds']} Players\n"
                f"{emoji_data['platform']['Xbox']} Xbox: {'{:,}'.format(data['AP']['X1']['val'])} RP | {data['AP']['X1']['totalMastersAndPreds']} Players\n"
                f"{emoji_data['platform']['Switch']} Switch: {'{:,}'.format(data['AP']['SWITCH']['val'])} RP | {data['AP']['SWITCH']['totalMastersAndPreds']} Players\n"
            ),
            inline=True
        )
        .set_footer(
            f"Requested by {ctx.member.display_name}",
            icon=ctx.member.display_avatar_url
        )
    )

    # Response
    await ctx.respond(embed)

def load(bot) -> None:
    bot.add_plugin(plugin)

def unload(bot) -> None:
    bot.remove_plugin(plugin)