# handlers/price.py

from aiogram import types
from aiogram.filters import Command
from services.binance import get_price


# ---------- HANDLE PRICE COMMAND ----------
async def price_handler(message: types.Message):
    """
    Handle /price command.
    Fetches the current price of the given cryptocurrency symbol and replies to the user.
    """
    # Split the incoming message into command arguments
    args = message.text.split()
    if len(args) < 2:
        # If no symbol provided, send usage example
        return await message.answer("ℹ Example: /price BTC")
    
    # Convert the symbol argument to uppercase for consistency
    symbol = args[1].upper()

    # Fetch the current price from Binance API
    price = await get_price(symbol)

    if price is not None:
        await message.answer(
        f"*📌 Live Price*\n\n"
        f"{symbol}/USDT\n"
        f"💲 {price:,.2f} dollars",
        parse_mode="Markdown"
    )
    else:
        await message.answer(f"🛑 Currency {symbol} not found or there is an error")
