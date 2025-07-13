import asyncio
import logging
import os

import discord

discord_token = os.getenv("DISCORD_TOKEN")
channel_id = os.getenv("DISCORD_CHANNEL_ID")

ready_event = asyncio.Event()


class DiscordClient(discord.Client):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.channel = None

    async def on_ready(self):
        print(f"We are ready to start, {self.user}")
        self.channel = self.get_channel(int(channel_id))
        if self.channel is None:
            print(f"Failed to find channel with id: {channel_id}")
        else:
            print("Ready to send messages")
        ready_event.set()

    async def send_message(self, text: str):
        await ready_event.wait()
        if self.channel:
            await self.channel.send(text)
        else:
            print("Channel not found")

    async def close(self):
        await super().close()
        print("Discord client closed")


handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

client = DiscordClient(intents=intents)


async def start_discord():
    if discord_token:
        await client.start(discord_token)
