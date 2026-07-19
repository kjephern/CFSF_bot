import discord
import logging
import os
import tomllib

from discord import app_commands
from discord.ext import commands
from pathlib import Path

from Bot.src.checker.permission import is_owner
from Bot.src.util.config import get_config

logger = logging.getLogger(__name__)


class Bot(commands.Bot):
    def __init__(self):
        self.config = get_config("general")
        prefix = self.config["bot.command_prefix"]
        super().__init__(command_prefix=prefix, intents=discord.Intents.all())

    async def setup_hook(self):
        logger.info("初始化機器人中...")
        await load_all_cogs(self)
        await self.tree.sync()

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
    parent_dir = Path(__file__).parent
    base_dirs = ["cogs", "src"]

    for base in base_dirs:
        dir_path = parent_dir / base

        if not dir_path.is_dir():
            logger.warning(f"資料夾不存在: {dir_path}，已跳過。")
            continue

        for path in dir_path.iterdir():
            is_py_file = path.is_file() and path.suffix == ".py" and path.name != "__init__.py"
            is_cog_package = path.is_dir() and (path / "__init__.py").exists()

            if is_py_file or is_cog_package:
                module_name = path.stem if is_py_file else path.name
                module_path = f"Bot.{base}.{module_name}"

                try:
                    await bot.load_extension(module_path)
                    logger.info(f"已載入 {module_name} 模組")
                except Exception as e:
                    logger.error(f"無法載入 {module_path}: {e}", exc_info=True)
