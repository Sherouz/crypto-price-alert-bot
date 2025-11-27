# bot.py - Initialize the bot, setup handlers, and start polling safely

import asyncio
import logging
from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram import Bot, exceptions
from config import BOT_TOKEN
from services.price_checker import price_checker
from utils.logger import log

# Import handlers
from handlers.start import start_handler
from handlers.price import price_handler
from handlers.alerts import up_handler, down_handler, list_handler, clear_handler
from handlers.help import help_handler

from services.shutdown import graceful_shutdown


# Reduce console spam: only show warnings/errors from aiogram & aiohttp
logging.getLogger("aiogram.event").setLevel(logging.WARNING)
logging.getLogger("aiogram.client").setLevel(logging.WARNING)
logging.getLogger("aiohttp").setLevel(logging.WARNING)


# ---------- GLOBAL TASK EXCEPTION HANDLER ----------
def handle_task_exception(task: asyncio.Task):
    """
    Retrieve the result of an asynchronous task and report any unhandled exceptions.

    This function is used as a done-callback for background asyncio tasks.  
    If the task finishes with an exception (other than being canceled), the
    exception is logged instead of being silently swallowed by asyncio.
    """
    try:
        task.result()
    except asyncio.CancelledError:
        pass  # safe to ignore
    except Exception as e:
        log.warning(f"Unhandled task exception: {e}")


# ---------- MAIN ENTRYPOINT & BOT STARTUP ----------
async def main():
    """
    Set up the Telegram bot lifecycle: initialize bot/configs,
    register handlers and middlewares,
    and start long-polling to process incoming updates.
    """
    
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Register handlers
    dp.message.register(start_handler, Command("start"))
    dp.message.register(price_handler, Command("price"))
    dp.message.register(up_handler, Command("up"))
    dp.message.register(down_handler, Command("down"))
    dp.message.register(list_handler, Command("list"))
    dp.message.register(clear_handler, Command("clear"))
    dp.message.register(help_handler, Command("help"))

    # Start background price checker
    task_checker = asyncio.create_task(price_checker(bot))
    task_checker.add_done_callback(handle_task_exception)

    # Wrap polling in a task so we can handle exceptions cleanly
    polling_task = asyncio.create_task(dp.start_polling(bot))
    polling_task.add_done_callback(handle_task_exception)


    try:
        # Wait for the polling task to run normally.
        await polling_task

    except exceptions.TelegramNetworkError as e:
        # Handle Telegram network-related issues (timeouts, disconnects, DNS failures).
        log.error(f"Network error: {e}")
    
    except KeyboardInterrupt:
        # Handle manual shutdown via Ctrl + C to stop the bot gracefully.
        log.info("KeyboardInterrupt received. Shutting down...")
    
    except Exception as e:
        # Catch any unexpected exceptions that were not explicitly handled.
        log.error(f"Unexpected error: {e}")
    
    finally:
        # Start the cleanup sequence and terminate background tasks.
        log.info("Stopping background tasks...")
        await graceful_shutdown(bot, task_checker, polling_task)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("KeyboardInterrupt: shutdown complete.")
