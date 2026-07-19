import discord

from discord import app_commands
from discord.ext import commands


from Bot.src.checker.permission import is_owner


class BotManage:
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @is_owner()
    @app_commands.command(name="sync", description="同步指令到伺服器")
    async def sync_command(self, itat: discord.Interaction):
        await itat.response.send_message("正在同步...")
        await itat.client.tree.sync()
        await itat.followup.send("同步完成！")
