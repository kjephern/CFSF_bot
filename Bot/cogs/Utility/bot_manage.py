import discord
import logging

from discord.ext import commands
from pathlib import Path
from typing import Literal, Optional


from Bot.src.checker.permission import is_owner
from Bot.src.util.cog import get_cog_list

logger = logging.getLogger(__name__)


class BotManage(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="sync", description="同步斜線指令到伺服器")
    @commands.guild_only()
    @commands.is_owner()
    async def sync_command(
        self,
        ctx: commands.Context,
        guilds: commands.Greedy[discord.Object],
        spec: Optional[Literal["~", "*", "^", "help"]] = None,
    ) -> None:
        """
        多功能指令同步工具。用法：
        !sync                        -> 全域同步
        !sync ~                      -> 同步到『當前伺服器』
        !sync *                      -> 將全域指令複製並同步到『當前伺服器』
        !sync ^                      -> 清除『當前伺服器』的同步指令
        !sync <GuildId1> <GuildID2>  -> 同步到指定 ID 的多個伺服器
        """

        if not guilds:
            if spec == "help":
                help_msg = (
                    "```"
                    + "!sync                        -> 全域同步\n"
                    + "!sync ~                      -> 同步到『當前伺服器\n"
                    + "!sync *                      -> 將全域指令複製並同步到『當前伺服器』\n"
                    + "!sync ^                      -> 清除『當前伺服器』的同步指令\n"
                    + "!sync <GuildId1> <GuildID2>  -> 同步到指定 ID 的多個伺服器\n"
                    + "```"
                )
                await ctx.send(content=help_msg)
                return
            msg = await ctx.send("正在同步中...")
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await msg.edit(
                content=f"已成功同步 {len(synced)} 個指令 " f"{'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await msg.edit(content=f"已成功將指令樹同步到 {ret}/{len(guilds)} 個伺服器。")

    @commands.command(name="load_cog")
    @commands.guild_only()
    @commands.is_owner()
    async def load_cog_command(self, ctx: commands.Context, *, cogs: str):
        cog_list = get_cog_list()
        to_load_cog = cogs.split(" ")
        for name in to_load_cog:
            path = cog_list.get(name)
            if path is None:
                continue
            try:
                await self.bot.load_extension(path)
                await ctx.send(f"已載入 {name} 模組")
                logger.info(f"已載入 {name} 模組")
            except Exception as e:
                await ctx.send(f"無法載入 {path}: {e}", exc_info=True)
                logger.error(f"無法載入 {path}: {e}", exc_info=True)

    @commands.command(name="unload_cog")
    @commands.guild_only()
    @commands.is_owner()
    async def unload_cog_command(self, ctx: commands.Context, *, cogs: str):
        cog_list = get_cog_list()
        to_unload_cog = cogs.split(" ")
        for name in to_unload_cog:
            path = cog_list.get(name)
            if path is None:
                continue
            try:
                await self.bot.unload_extension(path)
                await ctx.send(f"已卸載 {name} 模組")
                logger.info(f"已卸載 {name} 模組")
            except Exception as e:
                await ctx.send(f"無法卸載 {path}: {e}", exc_info=True)
                logger.error(f"無法卸載 {path}: {e}", exc_info=True)

    @commands.command(name="reload_cog")
    @commands.guild_only()
    @commands.is_owner()
    async def reload_cog_command(self, ctx: commands.Context, *, cogs: str):
        cog_list = get_cog_list()
        to_reload_cog = cogs.split(" ")
        for name in to_reload_cog:
            path = cog_list.get(name)
            if path is None:
                continue
            try:
                await self.bot.reload_extension(path)
                await ctx.send(f"已重新加載 {name} 模組")
                logger.info(f"已重新加載 {name} 模組")
            except Exception as e:
                await ctx.send(f"無法重新加載 {path}: {e}", exc_info=True)
                logger.error(f"無法重新加載 {path}: {e}", exc_info=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(BotManage(bot))
