# database/alerts.py

from typing import List, Dict
from utils.logger import log

alerts: List[Dict[str, object]] = []  # each dict: {"chat_id": int, "symbol": str, "price": float, "type": str}
inactive_users = set()  # Users who cleared all their alerts


# ---------- ADD NEW ALERT ----------
def add_alert(chat_id: int, symbol: str, price: float, alert_type: str):
    """Register a new price alert for the user."""
    global alerts, inactive_users
    
    # Add a new alert entry to the in-memory alerts list
    alerts.append({
        "chat_id": chat_id,
        "symbol": symbol,
        "price": price,
        "type": alert_type
    })
    
    # Activate user if they were previously inactive
    inactive_users.discard(chat_id)
    
    # Log successful creation of the alert for this user
    log.info(f"Alert added: User {chat_id} → {symbol} {alert_type.upper()} at {price:,.2f} USD")


# ---------- REMOVE ALERT ----------
def remove_alert(alert_item: dict):
    """Remove a specific alert from memory."""

    # Delete the alert item from the in-memory list
    alerts.remove(alert_item)

    # Extract all alert fields from the stored alert_item dict (chat_id, symbol, price, type)
    chat_id = alert_item["chat_id"]
    symbol = alert_item["symbol"]
    price = alert_item["price"]
    alert_type = alert_item["type"].upper()

    # Log successful removal of this alert for the user
    log.info(f"Alert removed: User {chat_id} → {symbol} {alert_type} at {price:,.2f} USD")


# ---------- GET USER ALERTS ----------
def get_user_alerts(chat_id: int):
    """Return all alerts for a specific user."""
    return [a for a in alerts if a["chat_id"] == chat_id]


# ---------- CLEAR USER ALERTS ----------
def clear_user_alerts(chat_id: int):
    """Clear all alerts for a user and mark them inactive."""
    global alerts, inactive_users
    
    before_count = len(alerts)
    alerts = [a for a in alerts if a["chat_id"] != chat_id]
    removed = before_count - len(alerts)
    
    if removed > 0:
        # Mark user as inactive to skip checks until a new alert is added
        inactive_users.add(chat_id)
        log.info(f"User {chat_id}: removed {removed} alerts → remaining: {len(alerts)}")
    
    return removed
