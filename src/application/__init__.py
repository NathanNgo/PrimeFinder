from discord.ext import commands
from settings import settings
from application.cogs.sacred_geometry_cog import SacredGeometry


def init_bot():
    bot = commands.Bot(command_prefix=settings.COMMAND_PREFIX)

    bot.add_cog(SacredGeometry(bot))

    # Register cogs here.
    return bot
