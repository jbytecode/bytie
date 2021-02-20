# bot.py
import messagehandle

import os
import ast


import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    incoming = message.content

    if incoming.startswith('hey bytie!'):
        response = messagehandle.bytie_handle_hey_bytie()
        await message.channel.send(response)

    if incoming.startswith("latex "):
        cmd = incoming[6:]
        response = messagehandle.bytie_handle_latex(cmd)
        await message.channel.send(response)

    if incoming.startswith("ast "):
        cmd = ast.parse(incoming[4:])
        result = messagehandle.bytie_handle_ast(cmd)
        await message.channel.send(result)
    
    if incoming.startswith("8ball "):
        cmd = incoming[6:]
        result = messagehandle.bytie_handle_8ball(cmd)
        await message.channel.send(result)


client.run(TOKEN)
