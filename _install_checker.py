#this file is run using the venv created by uv
import asyncio
import logging
import os
import subprocess
import sys
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession, MemorySession
from telethon.errors import (
    AuthKeyInvalidError,
    AccessTokenInvalidError,
    AccessTokenExpiredError,
    ChatWriteForbiddenError,
)

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("Stage 2")

CHECK_TIMEOUT = 20


async def telegram_user_check(string_session: str, api_id: int, api_hash: str) -> bool:
    logger.info("telegram_user_check")
    try:
        client = TelegramClient(StringSession(string_session), api_id, api_hash)
        await asyncio.wait_for(client.connect(), timeout=CHECK_TIMEOUT)
        try:
            if not await client.is_user_authorized():
                logger.error("User session is not authorized.")
                return False
            me = await asyncio.wait_for(client.get_me(), timeout=CHECK_TIMEOUT)
            return me is not None
        finally:
            await client.disconnect()
    except asyncio.TimeoutError:
        logger.error("User session check timed out.")
        return False
    except (AuthKeyInvalidError, ValueError) as e:
        logger.error("User session invalid: %s", e)
        return False
    except Exception as e:
        logger.error("User session check: %s", e)
        return False


async def telegram_bot_check(bot_token: str, api_id: int, api_hash: str) -> bool:
    logger.info("telegram_bot_check")
    try:
        client = await TelegramClient(MemorySession(), api_id, api_hash).start(bot_token=bot_token)
        async with client:
            me = await asyncio.wait_for(client.get_me(), timeout=CHECK_TIMEOUT)
            return me is not None
    except asyncio.TimeoutError:
        logger.error("Bot token check timed out.")
        return False
    except (AccessTokenInvalidError, AccessTokenExpiredError) as e:
        logger.error("Bot token invalid or expired: %s", e)
        return False
    except Exception as e:
        logger.error("Bot token check: %s", e)
        return False


async def check_bot_group_access(bot_token: str, api_id: int, api_hash: str, group_id: int) -> bool:
    logger.info("check_bot_group_access")
    client = await TelegramClient(MemorySession(), api_id, api_hash).start(bot_token=bot_token)
    try:
        await asyncio.wait_for(client.sendmessage(group_id, "Bot access check"), timeout=CHECK_TIMEOUT)
        return True
    except ChatWriteForbiddenError:
        logger.error("Bot doesn't have permission to send messages in the group.")
        return False
    except ValueError:
        logger.error("Group not found or bot is not a member.")
        return False
    except asyncio.TimeoutError:
        logger.error("Bot group send timed out.")
        return False
    except (AccessTokenInvalidError, AccessTokenExpiredError) as e:
        logger.error("Bot token invalid or expired: %s", e)
        return False
    except Exception as e:
        logger.error("Bot group access check: %s", e, exc_info=True)
        return False
    finally:
        await client.disconnect()


def is_database_operational(db_name="catuserbot", user="postgres") -> bool:
    logger.info("is_database_operational")
    try:
        subprocess.run(
            ["sudo", "-u", user, "psql", "-d", db_name, "-c", "SELECT 1;"],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
        return True
    except subprocess.TimeoutExpired:
        logger.error("Database check timed out.")
        return False
    except Exception as e:
        logger.error("Database check: %s", e)
        return False


async def main():
    logger.info("main")
    APP_ID         = os.getenv("APP_ID")
    API_HASH       = os.getenv("API_HASH")
    STRING_SESSION = os.getenv("STRING_SESSION")
    BOT_TOKEN      = os.getenv("TG_BOT_TOKEN")
    # GROUP_ID       = Development.PRIVATE_GROUP_BOT_API_ID

    checks = {
        "User session":await telegram_user_check(STRING_SESSION, APP_ID, API_HASH),
        "Bot token":await telegram_bot_check(BOT_TOKEN, APP_ID, API_HASH),
        # "Bot group access":await check_bot_group_access(BOT_TOKEN, APP_ID, API_HASH, GROUP_ID),
        "Database":is_database_operational(),
    }

    failed = [name for name, ok in checks.items() if not ok]
    if failed:
        logger.error("Checks failed: %s", ", ".join(failed))
        sys.exit(1)

    logger.info("All checks passed.")


if __name__ == "__main__":
    asyncio.run(main())

#End of the universe :)