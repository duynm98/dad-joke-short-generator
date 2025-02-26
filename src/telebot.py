import os

from dotenv import load_dotenv
import telepot
from loguru import logger

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = telepot.Bot(TELEGRAM_BOT_TOKEN)


def send_message(message: str):
    try:
        bot.sendMessage(chat_id=TELEGRAM_CHAT_ID, text=message)
        logger.info("Message sent to Telegram")
    except Exception as e:
        logger.error(f"Cannot send message to Telegram: {e}")


def send_video(video_path: str, caption: str = "Joke of the Day! #joke #jokeoftheday #comedy #dadjoke"):
    logger.info(f"Sending video {video_path} to Telegram. Caption: {caption}")
    try:
        bot.sendVideo(chat_id=TELEGRAM_CHAT_ID, video=open(video_path, "rb"), caption=caption)
        logger.success(f"Video {os.path.basename(video_path)} sent to Telegram")
    except Exception as e:
        logger.error(f"Cannot send video to Telegram {e}")
