# services/binance.py

from services.session import get_session
from utils.logger import log


# ---------- GET PRICE FROM BINANCE ----------
async def get_price(symbol: str) -> float | None:
    """
    Fetch the latest USDT price for a given symbol using Binance API.
    Returns the price as float on success, or None on API/network failure.
    """
    
    # Build Binance price URL
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}USDT"

    session = await get_session()   # shared session

    try:
        # Send GET request to Binance API
        async with session.get(url, timeout=10) as resp:

            # If request succeeded → parse JSON and extract price
            if resp.status == 200:
                data = await resp.json()     # Parse JSON response
                return float(data["price"])  # Convert price to float
            
            # Non-200 status → Binance returned an error
            else:
                log.warning(f"Binance error {resp.status} for {symbol}")
                return None
            
    # Network errors, timeout, JSON errors, etc.
    except Exception as e:
        log.error(f"Binance connection error for {symbol}: {e}")
        return None
