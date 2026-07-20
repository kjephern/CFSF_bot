import asyncio
import discord
import logging

from deep_translator import GoogleTranslator
from discord.ext import commands

logger = logging.getLogger(__name__)


def translator(text, source_lang, target_lang):
    return GoogleTranslator(source=source_lang, target=target_lang).translate(text)


class Translator:
    def __init__(self, bot: commands.Bot):
        self.bot = bot


class Translator:
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def _process_translation(self, ctx: commands.Context, text: str, src_lang: str, dest_lang: str):
        loading_msg = await ctx.reply("正在翻譯中，請稍候...")

        try:
            translated = await asyncio.to_thread(translator, text, src_lang, dest_lang)

            await send_webhook_message(text, translated, ctx)

            try:
                await loading_msg.delete()
            except:
                pass
            try:
                await ctx.message.delete()
            except:
                pass

        except discord.Forbidden:
            try:
                await loading_msg.delete()
            except:
                pass
            await ctx.send("機器人在本頻道缺少『管理 Webhook (Manage Webhooks)』權限！", delete_after=5)

        except Exception as e:
            logger.error(f"翻譯失敗 ({src_lang} -> {dest_lang}): {e}", exc_info=True)
            try:
                await loading_msg.edit(content="翻譯出現問題，請稍後再試", delete_after=3)
            except discord.NotFound:
                await ctx.send("翻譯出現問題，請稍後再試", delete_after=3)

    @commands.command(name="zh-en")
    async def chinese_to_english(self, ctx: commands.Context, *, text: str):
        await self._process_translation(ctx, text, "zh-TW", "en")

    @commands.command(name="zh-ja")
    async def chinese_to_japanese(self, ctx: commands.Context, *, text: str):
        await self._process_translation(ctx, text, "zh-TW", "ja")

    @commands.command(name="en-zh")
    async def english_to_chinese(self, ctx: commands.Context, *, text: str):
        await self._process_translation(ctx, text, "en", "zh-TW")

    @commands.command(name="en-ja")
    async def english_to_japanese(self, ctx: commands.Context, *, text: str):
        await self._process_translation(ctx, text, "en", "ja")

    @commands.command(name="ja-zh")
    async def japanese_to_chinese(self, ctx: commands.Context, *, text: str):
        await self._process_translation(ctx, text, "ja", "zh-TW")

    @commands.command(name="ja-en")
    async def japanese_to_english(self, ctx: commands.Context, *, text: str):
        await self._process_translation(ctx, text, "ja", "en")


async def get_or_create_webhook(channel: discord.TextChannel) -> discord.Webhook:
    """
    獲取頻道中現有的 Webhook，若沒有則新建一個。
    """
    webhooks = await channel.webhooks()
    for wh in webhooks:
        if wh.name == "Translator":
            return wh

    return await channel.create_webhook(name="Translator")


@staticmethod
async def send_webhook_message(text, translated_contex: str, ctx: commands.Context):
    webhook: discord.Webhook = await get_or_create_webhook(ctx.channel)
    await webhook.send(
        content=f"{translated_contex}\n\n-# Original content:{text}",
        username=ctx.author.display_name,
        avatar_url=ctx.author.display_avatar.url,
    )
