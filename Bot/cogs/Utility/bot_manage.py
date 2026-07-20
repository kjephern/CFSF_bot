import discord

from discord.ext import commands
from typing import Literal, Optional


from Bot.src.checker.permission import is_owner


class BotManage:
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
