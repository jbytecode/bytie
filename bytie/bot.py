# bot.py
from messagehandle import message_handlers

import os
import ast
import random


import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client()


@client.event
async def on_ready():
    print(f"{client.user.name} has connected to Discord!")


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f"Hi {member.name}, welcome to my Discord server!")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    incoming = message.content

    if incoming.startswith("bytie shutdown!"):
        await message.channel.send("Goodbye cruel world!")
        exit()

    for handler in message_handlers:
        msg = handler['handler'](incoming)
        if msg:
            await message.channel.send(msg)


client.run(TOKEN)
