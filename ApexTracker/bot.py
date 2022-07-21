import logging
import os
import aiosqlite
from pytz import utc
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiohttp import ClientSession
import hikari
import lightbulb
import sake

# Instantiate Logging
log = logging.getLogger(__name__)

# Instantiate a Bot instance
bot = lightbulb.BotApp(
    token=os.environ["TOKEN"], 
    prefix="!", 
    # default_enabled_guilds=int(os.environ["DEFAULT_GUILD_ID"]),
    default_enabled_guilds=(993472099463213096, 659183353202737152, 405121285195300875),
    help_slash_command=True,
    case_insensitive_prefix_commands=True,
    intents=hikari.Intents.ALL
    )

bot.d.scheduler = AsyncIOScheduler()
bot.d.scheduler.configure(timezone=utc)
logging.getLogger('apscheduler.executors.default').setLevel(logging.WARNING)

bot.load_extensions_from("./ApexTracker/extensions")

""" EVENTS """
@bot.listen(hikari.StartingEvent)
async def on_starting(event: hikari.StartingEvent) -> None:

    # Create database
    bot.d.db = await aiosqlite.connect(database="./data/database.sqlite3")
    await bot.d.db.execute("pragma journal_mode=wal")
    with open("./data/build.sql") as f:
        await bot.d.db.execute(f.read())
    bot.d.scheduler.add_job(bot.d.db.commit, CronTrigger(second=0))
    log.info("Database connection opened.")

    # Create cache
    cache = sake.redis.RedisCache(app=bot, address="redis://localhost:6379")
    await cache.open()
    log.info("Connected to Redis Server.")
    
    # Create objects
    bot.d.scheduler.start()
    bot.d.session = ClientSession(trust_env=True)
    log.info("AIOHTTP session started.")

@bot.listen(hikari.StartedEvent)
async def on_started(event: hikari.StartedEvent) -> None:
    bot.d.scheduler.add_job(
        lambda: log.info(f"Ping: {bot.heartbeat_latency * 1000:.0f} ms"),
        CronTrigger(second="*/15"), # logs every 15seconds now
    )

    await bot.rest.create_message(
        channel=int(os.environ["STDOUT_CHANNEL_ID"]), 
        content="Apex Tracker Bot is Online."
    )

@bot.listen(hikari.StoppingEvent)
async def on_stopping(event: hikari.StoppingEvent) -> None:
    bot.d.scheduler.shutdown()
    await bot.d.session.close()
    log.info("AIOHTTP session closed.")

    await bot.d.db.close()
    log.info("Database connection closed.")

    await bot.rest.create_message(
        channel=int(os.environ["STDOUT_CHANNEL_ID"]),
        content="Apex Tracker Bot is now Offline."
    )

""" ERROR HANDELING """
@bot.listen(hikari.ExceptionEvent)
async def on_error(event: hikari.ExceptionEvent) -> None:
    raise event.exception

@bot.listen(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent) -> None:

    if  isinstance(event.exception, lightbulb.CommandNotFound):
        # when command is attempted to be invoked but no implementation is available
        # Only for prefix commands
        return
    
    if isinstance(event.exception, lightbulb.CommandIsOnCooldown):
        await event.context.respond(
            "Command is on cooldown. Wait "
            "f{event.exception.retry_after:.0f} seconds, then try again."
        )
        return

    if isinstance(event.exception, lightbulb.ConverterFailure):
        await event.context.respond(
            f"The '{event.exception.option}' option is invalid."
        )

    if isinstance(event.exception, lightbulb.NotEnoughArguments):
        await event.context.respond(
            "There are some missing arguments: " + ", ".join(o.name for o in event.exception.missing_options)
        )
        return

    await event.context.respond("Something went wrong.")

    if isinstance(event.exception, lightbulb.CommandInvocationError):
        raise event.exception.original

    raise event.exception


def run() -> None:
    if os.name != 'nt':
        import uvloop
        uvloop.install()
    
    bot.run()
