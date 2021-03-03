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
async def on_group_join(channel, user):
    await channel.send(f"{user} is here! :man_detective:")


@client.event
async def on_group_remove(channel, user):
    await channel.send(f"{user} is out! :man_detective:")


@client.event
async def on_typing(channel: discord.abc.Messageable, user, when):
    if random.random() < 0.025:
        await channel.send(f"{user} is typing something :rolling_eyes:")


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
