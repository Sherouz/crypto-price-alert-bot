# services/price_checker.py - Stops tracking immediately when no alerts left

import asyncio
from typing import Dict
from aiogram import Bot
from database.alerts import alerts, remove_alert
from services.binance import get_price
from utils.logger import log
from database.alerts import inactive_users
from config import CHECK_INTERVAL


# ---------- PRICE CHECKING BACKGROUND TASK ----------
async def price_checker(bot: Bot):
    """Continuously check prices and trigger alerts for active users only."""
    log.info(f"Price checking task started — interval: {CHECK_INTERVAL}s")

    try:
        while True:
            if not alerts:
                await asyncio.sleep(CHECK_INTERVAL)
                continue

            # Only check symbols for users who are not inactive
            active_alerts = [a for a in alerts if a["chat_id"] not in inactive_users]
            if not active_alerts:
                await asyncio.sleep(CHECK_INTERVAL)
                continue

            symbols = {a["symbol"] for a in active_alerts}
            prices = {}

            for sym in symbols:
                price = await get_price(sym)
                if price is not None:
                    prices[sym] = price
                await asyncio.sleep(0.5)

            triggered = []
            for alert in active_alerts[:]:  # Copy to avoid deletion issues
                if alert["symbol"] in prices:
                    current = prices[alert["symbol"]]
                    if (alert["type"] == "up" and current >= alert["price"]) or \
                       (alert["type"] == "down" and current <= alert["price"]):

                        await bot.send_message(
                            alert["chat_id"],
                            f"⚠️ Price Alert!\n\n"
                            f"{alert['symbol']}/USDT has reached your target!\n"
                            f"Current price: {current:,.4f} USD\n"
                            f"Target: {'above' if alert['type']=='up' else 'below'} {alert['price']:,.0f}"
                        )
                        triggered.append(alert)

            for t in triggered:
                remove_alert(t)

            await asyncio.sleep(CHECK_INTERVAL)
    except asyncio.CancelledError:
        log.info("Price checker task cancelled.")
        raise