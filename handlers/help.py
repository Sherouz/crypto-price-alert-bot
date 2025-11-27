# handlers/help.py

from aiogram import types
from aiogram.filters import Command

# ---------- HELP COMMAND HANDLER ----------
async def help_handler(message: types.Message):
    """Provide full usage instructions, command descriptions, and examples."""
    
    text = (
        "📘 **Help Menu — How to use the Coin Tracker Bot**\n\n"
        
        "Use the commands below to get prices or set alerts:\n\n"

        "• /price SYMBOL\n"
        "  Get the current market price of a cryptocurrency.\n"
        "  Example: `/price BTC`\n\n"

        "• /up SYMBOL TARGET_PRICE\n"
        "  Alert triggers when the price goes *above* the target.\n"
        "  Example: `/up BTC 65000`\n\n"

        "• /down SYMBOL TARGET_PRICE\n"
        "  Alert triggers when the price goes *below* the target.\n"
        "  Example: `/down ETH 3000`\n\n"

        "• /list\n"
        "  Shows all active alerts you have.\n"
        "  Useful when you've set multiple alerts.\n\n"

        "• /clear\n"
        "  Deletes all your alerts at once.\n"
        "  Use carefully — this cannot be undone.\n\n"

        "• /help\n"
        "  Shows the full help menu with all commands and examples.\n"
        "  Useful when you need a quick reminder of how things work.\n\n"


        "ℹ️ Alerts are checked automatically in the background.\n"
        "You will receive a message the moment your price condition is met."
    )

    await message.answer(text, parse_mode="Markdown")
