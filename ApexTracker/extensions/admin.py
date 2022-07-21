import lightbulb
from lightbulb import commands
plugin = lightbulb.Plugin("Admin")

@plugin.command()
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command("shutdown", "Shutdown the bot.", ephemeral=True)
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def cmd_shutdown(ctx) -> None:
    # await ctx.respond("The bot has shutdown.")
    await ctx.bot.close()

def load(bot) -> None:
    bot.add_plugin(plugin)

def unload(bot) -> None:
    bot.remove_plugin(plugin)