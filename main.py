# coding: utf-8
from ctypes import *
from dotenv import load_dotenv
import os
import discord

# 環境変数の読み込み
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_APIKEY = os.getenv('OPENAI_APIKEY')

# bot command
BOT_COMMAND = '!gpo'

# 共有ライブラリの読み込み
lib = cdll.LoadLibrary("./shared/ojosama.dll")

ojosama = lib.convertOjosama
ojosama.argtypes = [c_char_p]
ojosama.restype = c_char_p


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('ログインしました')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(BOT_COMMAND):
        msg = message.content.replace(BOT_COMMAND, '').encode('utf-8')
        msg = ojosama(msg).decode('utf-8')
        await message.channel.send(msg)

client.run(DISCORD_TOKEN)
