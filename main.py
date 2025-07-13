import asyncio
import os

import asyncpraw
from dotenv import load_dotenv

from discord_setup import client, start_discord

load_dotenv()


async def monitor_reddit():
    reddit = asyncpraw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent="Reddit Post Notification Bot",
    )
    subreddit = await reddit.subreddit("fantasyromance")

    async for submission in subreddit.stream.submissions():
        if "Editor Read" in submission.title:
            await client.send_message(
                f"New submission from XusBookReviews: {submission.title}\nhttps://reddit.com{submission.permalink}"
            )


async def main():
    await asyncio.gather(start_discord(), monitor_reddit())


if __name__ == "__main__":
    asyncio.run(main())
