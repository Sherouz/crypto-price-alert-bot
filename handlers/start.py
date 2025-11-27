# handlers/start.py

from aiogram import types
from aiogram.filters import Command
from config import CHECK_INTERVAL

# ---------- START COMMAND HANDLER ----------
async def start_handler(message: types.Message):
    """Send a short welcome message with a brief description of the bot."""
    text = (
        "🚀 Welcome to *Coin Tracker Bot*!\n\n"
        "This bot provides cryptocurrency price alerts and notifications.\n"
        f"Prices are updated every {CHECK_INTERVAL} seconds.\n\n"
        "Use */help* to see all available commands and examples."
    )
    
    await message.answer(text, parse_mode="Markdown")
