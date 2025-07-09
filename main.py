import os
import time
import logging
import praw
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

discord_token = os.getenv("DISCORD_TOKEN")

# Set up reddit
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    password=os.getenv("REDDIT_PASSWORD"),
    user_agent="Reddit Post Notification Bot",
    username=os.getenv("REDDIT_USERNAME"),
)

# Set up variables
SUBREDDIT = os.getenv("SUBREDDIT")
POST_TITLE = os.getenv("POST_TITLE")
POST_BODY = os.getenv("POST_BODY")
INTERVAL = os.getenv("INTERVAL")

while True:
    # Get new posts
    new_posts = reddit.subreddit(SUBREDDIT).new(limit=100)

    # Check if new posts exist
    if new_posts:
        # Loop through new posts
        for post in new_posts:
            # Check if post title matches
            if post.title == POST_TITLE:
                # Check if post body matches
                if post.selftext == POST_BODY:
                    # Sleep for interval
                    time.sleep(int(INTERVAL))
