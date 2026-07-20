from discord.ext import commands

from Bot.cogs.Utility.bot_manage import BotManage
from Bot.cogs.Utility.translator import Translator


class Utility(commands.Cog, BotManage, Translator):
    def __init__(self, bot: commands.Bot):
        commands.Cog.__init__(self)
        BotManage.__init__(self, bot)
        Translator.__init__(self, bot)


async def setup(bot: commands.Bot):
    await bot.add_cog(Utility(bot))
