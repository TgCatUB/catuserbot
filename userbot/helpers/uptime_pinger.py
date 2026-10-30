import urllib.parse

import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from userbot import LOGS

from ..Config import Config

PING_URL_FROM_ENV = Config.UPTIME_PING_URL

if PING_URL_FROM_ENV:
    parsed_url = urllib.parse.urlparse(PING_URL_FROM_ENV)
    DOMAIN_ONLY = parsed_url.netloc  # Only the domain
    PING_URL = f"{parsed_url.scheme}://{parsed_url.netloc}/status"
else:
    DOMAIN_ONLY = None
    PING_URL = None


async def ping():
    """Async ping function to avoid blocking"""
    if not PING_URL:
        LOGS.info("[UPTIME PINGER] No PING_URL set, skipping ping")
        return
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=10) as client:
            response = await client.get(PING_URL)
        LOGS.info(f"[UPTIME PINGER] Pinged {PING_URL} - Status {response.status_code}")
    except Exception as e:
        LOGS.warning(f"[UPTIME PINGER] Failed: {e}")


def start_uptime_pinger():
    if not PING_URL_FROM_ENV:
        LOGS.info("[UPTIME PINGER] No UPTIME_PING_URL set, skipping uptime pinger")
        return None

    LOGS.info(f"[UPTIME PINGER] Initiated for domain: {DOMAIN_ONLY}")
    scheduler = AsyncIOScheduler()
    scheduler.add_job(ping, "interval", minutes=7)
    scheduler.start()
    return scheduler
