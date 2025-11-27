# services/shutdown.py

import asyncio
from utils.logger import log
from services.session import get_session

async def graceful_shutdown(bot, task_checker, polling_task):
    log.info("Stopping background tasks...")

    # Cancel tasks
    task_checker.cancel()
    polling_task.cancel()
    await asyncio.gather(task_checker, polling_task, return_exceptions=True)

    # Close bot session
    try:
        await bot.session.close()
    except:
        pass

    # Close shared session
    session = await get_session()
    try:
        await session.close()
    except:
        pass
