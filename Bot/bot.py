import discord
import logging

from discord.ext import commands
from pathlib import Path

from Bot.src.util.cog import get_cog_list
from config.config import get_config

logger = logging.getLogger(__name__)


class Bot(commands.Bot):
    def __init__(self):
        self.config = get_config("general")
        prefix = self.config["bot.command_prefix"]
        super().__init__(command_prefix=prefix, intents=discord.Intents.all(), help_command=None)

    async def setup_hook(self):
        logger.info("初始化機器人中...")
        await load_all_cogs(self)

    async def on_ready(self):
        logger.info(f"以{self.user.name} - {self.user.id}登入")
        logger.info("已連接至以下伺服器")
        for guild in self.guilds:
            logger.info(f" - {guild.name} (ID: {guild.id})")

    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CommandNotFound):
            return

        await super().on_command_error(ctx, error)


async def load_all_cogs(bot: commands.Bot):
    cogs = get_cog_list()
    for name, path in cogs.items():
        try:
            await bot.load_extension(path)
            logger.info(f"已載入 {name} 模組")
        except Exception as e:
            logger.error(f"無法載入 {path}: {e}", exc_info=True)
