import asyncio
import os
import signal

import asyncpraw

from discord_setup import client, start_discord


async def monitor_reddit(reddit):
    subreddit = await reddit.subreddit("fantasyromance")

    async for submission in subreddit.stream.submissions():
        if "Editor Read" in submission.title:
            await client.send_message(
                f"New submission from XusBookReviews: {submission.title}\nhttps://reddit.com{submission.permalink}"
            )


async def main():
    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stop_event.set)

    reddit = asyncpraw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent="Reddit Post Notification Bot",
    )

    monitor_task = asyncio.create_task(monitor_reddit(reddit))
    discord_task = asyncio.create_task(start_discord())

    await stop_event.wait()

    # On signal, cancel tasks and cleanup
    monitor_task.cancel()
    discord_task.cancel()

    await reddit.close()
    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
