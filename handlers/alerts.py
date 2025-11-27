# handlers/alerts.py - Smart & user-friendly

from aiogram import types, Bot
from aiogram.filters import Command
from database.alerts import add_alert, get_user_alerts, clear_user_alerts
from services.binance import get_price


# ---------- HANDLE /UP COMMAND ----------
async def up_handler(message: types.Message):
    """Handle /up command and create an upward alert."""
    await _create_alert(message, "up", "up")


# ---------- HANDLE /DOWN COMMAND ----------
async def down_handler(message: types.Message):
    """Handle /down command and create a downward alert."""
    await _create_alert(message, "down", "down")


# ---------- MAIN HANDLER ----------
async def _create_alert(message: types.Message, alert_type: str, direction_text: str):
    """Main orchestrator for creating alerts."""

    parsed = await _parse_and_validate(message, alert_type)
    if parsed is None:
        return
    symbol, target_price = parsed

    current_price = await get_price(symbol)
    if current_price is None:
        return await message.answer(f"I can't fetch the current price of {symbol} from Binance. Try again.")

    # Check if alert would immediately trigger
    if await _check_alert_immediate(
        message, alert_type, symbol, current_price, target_price
    ):
        return

    # Check for unrealistic/mistyped prices
    if await _check_common_mistakes(
        message, symbol, current_price, target_price, direction_text
    ):
        return

    # Save alert
    add_alert(message.chat.id, symbol, target_price, alert_type)

    return await message.answer(
        f"✔ Alert successfully registered!\n\n"
        f"{symbol}/USDT now: {current_price:,.4f} dollars\n"
        f"When it goes {direction_text} {target_price:,} → I'll notify you."
    )


# ---------- 1) VALIDATION ----------
async def _parse_and_validate(message: types.Message, alert_type: str):
    """Validate symbol and target price from user input."""
    args = message.text.split()

    if len(args) != 3:
        await message.answer(f"ℹ Example: /{alert_type} BTC 65000")
        return None

    symbol = args[1].upper()

    try:
        target_price = float(args[2])
        if target_price <= 0:
            raise ValueError
    except ValueError:
        await message.answer("The price must be a positive number!")
        return None

    return symbol, target_price


# ---------- 2) CHECK IF ALERT WOULD TRIGGER NOW ----------
async def _check_alert_immediate(message, alert_type, symbol, current_price, target_price):
    """Check if alert criteria already satisfied right now."""
    if alert_type == "up" and current_price >= target_price:
        reason = f"Current price is *{current_price:,.4f}* — above *{target_price:,}*"
    elif alert_type == "down" and current_price <= target_price:
        reason = f"Current price is *{current_price:,.4f}* — below *{target_price:,}*"
    else:
        return False

    await message.answer(
        f"*This alert would trigger immediately! ⚠*\n\n"
        f"{symbol}/USDT now: *{current_price:,.4f}*\n"
        f"{reason}\n\n"
        f"Alert not added because the target is _already_ reached.",
        parse_mode="Markdown"
    )
    return True


# ---------- 3) CHECK FOR COMMON USER MISTAKES ----------
async def _check_common_mistakes(message, symbol, current_price, target_price, direction_text):
    """Detect common mistakes such as missing decimals or unrealistic targets."""

    # e.g. SOL price = 4$ → user writes 4000$
    if target_price > 10000 and current_price < 10:
        suggestion = f"Maybe you meant {target_price/100:.2f} or {target_price/1000:.4f}?"
        await message.answer(
            f"Warning!\n"
            f"The current price of {symbol} is only {current_price:,.4f}\n"
            f"But you asked for {direction_text} {target_price:,}!\n\n"
            f"{suggestion}\n"
            f"If you're sure, send it again."
        )
        return True

    # e.g. BTC = 40,000$ → user writes 40$
    if target_price < 100 and current_price > 10000:
        suggestion = f"Maybe you meant {target_price * 1000:,}?"
        await message.answer(
            f"Warning!\n"
            f"{symbol} is currently around {current_price:,.0f} dollars\n"
            f"But you set the target to {direction_text} {target_price:,}!\n\n"
            f"{suggestion}\n"
            f"If you're sure, send it again."
        )
        return True

    return False


# ---------- HANDLE /LIST COMMAND ----------
async def list_handler(message: types.Message):
    """Show all active alerts for the user."""
    
    # Get alerts for this user
    user_alerts = get_user_alerts(message.chat.id)
    if not user_alerts:
        return await message.answer("You have no warning.")

    text = "*📃 Your active alerts:*\n\n"

    # Build alerts text
    for i, a in enumerate(user_alerts, 1):
        direction = "up" if a["type"] == "up" else "down"
        text += f"{i}. {a['symbol']} {direction} {a['price']:,.0f}\n"
    await message.answer(text, parse_mode="Markdown")
    

# ---------- CLEAR USER ALERTS ----------
async def clear_handler(message: types.Message):
    """Clear all alerts for the current user and notify them."""
    removed = clear_user_alerts(message.chat.id)
    
    if removed == 0:
        await message.answer("You have no alerts to clear!")
    else:
        await message.answer(f"🧹 All {removed} of your alerts have been cleared!")
