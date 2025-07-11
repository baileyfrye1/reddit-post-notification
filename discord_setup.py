import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

discord_token = os.getenv("DISCORD_TOKEN")


# Convert below to a class for more OOP approach and for better usability in other files
class DiscordClient(discord.Client):
    async def on_ready(self):
        print(f"We are ready to start, {self.user}")

    async def on_message(self, message):
        if message.author == self.user:
            return


# Set up Discord
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = DiscordClient(intents=intents)
if discord_token is not None:
    client.run(discord_token, log_handler=handler, log_level=logging.DEBUG)

user = client.get_user(1127378884564897873)
