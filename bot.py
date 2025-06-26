import os
import logging
import asyncio
import nest_asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.error import BadRequest

# === Load .env file ===
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# === Required Channels ===
REQUIRED_CHANNELS = [
    "@MythicVoiceTamil",       # Public
    "-1002624986156"           # Private
]

# === Logging ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Bot Handler ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    not_joined = []

    for channel in REQUIRED_CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel, user_id=user.id)
            if member.status not in ['member', 'administrator', 'creator']:
                not_joined.append(channel)
        except BadRequest:
            not_joined.append(channel)

    if not_joined:
        await prompt_join_channels(update, not_joined)
    else:
        await update.message.reply_text("✅ Access granted! Welcome to the bot.")

async def prompt_join_channels(update: Update, channels):
    links = "\n".join([f"👉 [Join Here]({make_channel_link(c)})" for c in channels])
    await update.message.reply_text(
        f"🚫 Please join these channels to use the bot:\n\n{links}\n\nThen press /start again.",
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )

def make_channel_link(channel_id):
    if channel_id.startswith("@"):
        return f"https://t.me/{channel_id.strip('@')}"
    elif channel_id.startswith("-100"):
        return f"https://t.me/c/{channel_id[4:]}"
    return "https://t.me/"

# === Main Bot Setup ===
async def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("🤖 Bot is running... Press Ctrl+C to stop.")
    await app.run_polling()

# === Entrypoint (with patched loop) ===
if __name__ == "__main__":
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_bot())
