from discord.ext import commands
from settings import settings


def init_bot():
    bot = commands.Bot(command_prefix=settings.COMMAND_PREFIX)

    # Register cogs here.
    return bot
