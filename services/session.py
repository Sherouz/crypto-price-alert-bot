# services/session.py

import aiohttp

session: aiohttp.ClientSession | None = None  # global shared


# ---------- GET OR CREATE SHARED AIOHTTP SESSION ----------
async def get_session() -> aiohttp.ClientSession:
    """
    Return a global aiohttp session.
    Creates a new session only if none exists or the previous one is closed.
    """
    global session

    if session is None or session.closed:
        session = aiohttp.ClientSession()

    return session