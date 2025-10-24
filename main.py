import asyncio
import logging
import os
import signal

import asyncpraw

from discord_setup import client, start_discord

shutdown_event = asyncio.Event()

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)

logger = logging.getLogger(__name__)


async def monitor_reddit(reddit):
    subreddit = await reddit.subreddit("fantasyromance")
    async for submission in subreddit.stream.submissions():
        if "Editor Read" in submission.title:
            await client.send_message(
                f"New submission from XusBookReviews: {submission.title}\nhttps://reddit.com{submission.permalink}"
            )
        else:
            logger.info("No new submission found")
        if shutdown_event.is_set():
            break


async def handle_signals():
    for sig in (signal.SIGINT, signal.SIGTERM):
        asyncio.get_running_loop().add_signal_handler(sig, shutdown_event.set)


async def connect_reddit_with_retries(max_retries=5):
    for attempt in range(1, max_retries + 1):
        try:
            reddit = asyncpraw.Reddit(
                client_id=os.getenv("REDDIT_CLIENT_ID"),
                client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
                user_agent="Reddit Post Notification Bot",
            )
            await reddit.user.me()
            return reddit
        except Exception as e:
            logger.warning(f"Retry {attempt}: Reddit connection failed: {e}")
            await asyncio.sleep(2**attempt)
    raise RuntimeError("Reddit connection failed after max retries.")


async def main():
    await handle_signals()
    reddit = await connect_reddit_with_retries()

    async with asyncio.TaskGroup() as tg:
        tg.create_task(monitor_reddit(reddit))
        tg.create_task(start_discord())

        await shutdown_event.wait()
        logger.info("Shutdown initiated...")

    await reddit.close()
    await client.close()

    logger.info("Graceful shutdown complete.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.error("Forced shutdown.")
