import asyncio
import os

import asyncpraw as praw
from dotenv import load_dotenv

from discord_setup import user

load_dotenv()

# Initilize Reddit instance
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent="Reddit Post Notification Bot",
)


async def send_message():
    subreddit = await reddit.subreddit("fantasyromance")
    for submission in subreddit.stream.submissions():
        if "Editor Read" in submission.title:
            await user.send(
                f"New submission from XusBookReviews: {submission.title}\nhttps://reddit.com{submission.peramlink}"
            )


if __name__ == "__main__":
    asyncio.run(send_message())
