import asyncio
import discord
import logging

from deep_translator import GoogleTranslator
from discord import app_commands
from discord.ext import commands

from config.config import get_config

config = get_config("translator")
logger = logging.getLogger(__name__)


class Translator:
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="zh-en")
    async def chinese_to_english(self, ctx: commands.Context, *, text: str):
        await _process_single_translation(ctx, text, "zh-TW", "en")

    @commands.command(name="zh-ja")
    async def chinese_to_japanese(self, ctx: commands.Context, *, text: str):
        await _process_single_translation(ctx, text, "zh-TW", "ja")

    @commands.command(name="en-zh")
    async def english_to_chinese(self, ctx: commands.Context, *, text: str):
        await _process_single_translation(ctx, text, "en", "zh-TW")

    @commands.command(name="en-ja")
    async def english_to_japanese(self, ctx: commands.Context, *, text: str):
        await _process_single_translation(ctx, text, "en", "ja")

    @commands.command(name="ja-zh")
    async def japanese_to_chinese(self, ctx: commands.Context, *, text: str):
        await _process_single_translation(ctx, text, "ja", "zh-TW")

    @commands.command(name="ja-en")
    async def japanese_to_english(self, ctx: commands.Context, *, text: str):
        await _process_single_translation(ctx, text, "ja", "en")

    @commands.command(name="tzh")
    async def translate_chinese(self, ctx: commands.Context, *, text: str):
        src_lang = "zh-TW"
        await _process_multi_translation(ctx, text, "zh-TW")


async def get_or_create_webhook(channel: discord.TextChannel) -> discord.Webhook:
    """
    獲取頻道中現有的 Webhook，若沒有則新建一個。
    """
    webhooks = await channel.webhooks()
    for wh in webhooks:
        if wh.name == "Translator":
            return wh

    return await channel.create_webhook(name="Translator")


async def _process_single_translation(ctx: commands.Context, text: str, src_lang: str, dest_lang: str):
    loading_msg = await ctx.reply("正在翻譯中，請稍候...")

    try:
        translated = await asyncio.to_thread(translator, text, src_lang, dest_lang)
        content = f"{translated}\n-# Original content: {text}"
        await send_webhook_message(content, ctx)

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


async def _process_multi_translation(ctx: commands.Context, text: str, src_lang: str):
    loading_msg = await ctx.reply("正在翻譯中，請稍候...")

    try:
        supported_languages = config["supported_languages"]
        content = ""
        for dest_lang in supported_languages:
            if dest_lang == src_lang:
                continue
            content += await asyncio.to_thread(translator, text, src_lang, dest_lang) + "\n\n"
        content += text
        await send_webhook_message(content, ctx)

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


async def send_webhook_message(text: str, ctx: commands.Context):
    webhook: discord.Webhook = await get_or_create_webhook(ctx.channel)
    await webhook.send(
        content=text,
        username=ctx.author.display_name,
        avatar_url=ctx.author.display_avatar.url,
    )


def translator(text, source_lang, target_lang):
    return GoogleTranslator(source=source_lang, target=target_lang).translate(text)
