# utils/logger.py - Logging settings

import logging
import sys
from pathlib import Path

# ---------- SETUP LOGGER ----------
def setup_logger(
    name: str = "Coin Tracker Bot",
    log_file: str = "logs/crypto_alert_bot.log",
    console_level=logging.INFO,
    file_level=logging.DEBUG
) -> logging.Logger:
    """
    Configure and return the main logger for CryptoAlertBot.
    
    Features:
    - INFO level for console, DEBUG level for file logging
    - Standard formatter with full timestamp
    - Prevents duplicate handlers
    - Logs both to console and file
    """
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # base level

    # Prevent duplicate handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # Formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d | %H:%M:%S"
    )

    # ---------- Console Handler ----------
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(console_level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # ---------- File Handler ----------
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)  # make sure folder exists

    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(file_level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger

# Ready-to-use logger
log = setup_logger()
