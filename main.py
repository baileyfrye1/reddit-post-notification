import asyncio
import os
import signal

import asyncpraw

from discord_setup import client, start_discord

shutdown_event = asyncio.Event()


async def monitor_reddit(reddit):
    subreddit = await reddit.subreddit("fantasyromance")
    async for submission in subreddit.stream.submissions():
        if "Editor Read" in submission.title:
            await client.send_message(
                f"New submission from XusBookReviews: {submission.title}\nhttps://reddit.com{submission.permalink}"
            )
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
            print(f"Retry {attempt}: Reddit connection failed: {e}")
            await asyncio.sleep(2**attempt)
    raise RuntimeError("Reddit connection failed after max retries.")


async def main():
    await handle_signals()
    reddit = await connect_reddit_with_retries()

    reddit_task = asyncio.create_task(monitor_reddit(reddit))
    discord_task = asyncio.create_task(start_discord())

    await shutdown_event.wait()
    print("Shutdown initiated...")

    reddit_task.cancel()
    discord_task.cancel()

    await asyncio.gather(reddit_task, discord_task, return_exceptions=True)
    await reddit.close()
    await client.close()

    print("Graceful shutdown complete.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Forced shutdown.")
