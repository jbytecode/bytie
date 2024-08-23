# bot.py
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
        response = "Yes sir!"
        await message.channel.send(response)

    if incoming.startswith("$$"):
        response = "I didn't yet implement the LaTeX rendering, sir!"
        await message.channel.send(response)

    if  incoming.startswith("ast "):
        tree = ast.parse(incoming[4:])
        result = ast.dump(tree)
        await message.channel.send(result)


client.run(TOKEN)


