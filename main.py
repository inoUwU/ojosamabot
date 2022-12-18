# coding: utf-8
from ctypes import *
from dotenv import load_dotenv
import os
import discord
import openai

# 環境変数の読み込み
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
openai.api_key = os.getenv('OPENAI_APIKEY')

# bot command
BOT_COMMAND = '!po'

# 共有ライブラリの読み込み
lib = cdll.LoadLibrary("./shared/ojosama.dll")

ojosama = lib.convertOjosama
ojosama.argtypes = [c_char_p]
ojosama.restype = c_char_p

# bot 設定
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


def fetch_answer(question: str):
    prompt = f'''私は真実を答える賢い質問応答ボットです。 
    Q: 日本の人口は？
    A: 約1億人です。
    Q: {question}？
    A: '''

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\n"]
    )
    print(response)
    return response['choices'][0]['text']


@client.event
async def on_ready():
    print('ログインしました')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(BOT_COMMAND):
        question = message.content.replace(BOT_COMMAND, '').strip()
        ans = fetch_answer(question=question)
        res_msg = ojosama(ans.encode('utf-8')).decode('utf-8')
        await message.channel.send(res_msg, reference=message)

client.run(DISCORD_TOKEN)
