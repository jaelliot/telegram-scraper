import os
from telethon import TelegramClient
from dotenv import load_dotenv
from config import settings
from handlers import register_handlers
import logging

# Load environment variables
load_dotenv()

# Initialize the client
client = TelegramClient('bot', settings.api_id, settings.api_hash).start(bot_token=settings.bot_token)

# Ensure the download path exists
os.makedirs(settings.download_path, exist_ok=True)

# Register event handlers
register_handlers(client)

# Start the client
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Bot is running...")

client.run_until_disconnected()
