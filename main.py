import discord
from discord.ext import commands
import asyncio
import os
import yt_dlp as youtube_dl
from youtubesearchpython import VideosSearch

import config

intents = discord.Intents.default()
intents.all()

intents.messages = True  # Включаем интенты для сообщений
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'opus',
        'preferredquality': '192',
    }],
    'outtmpl': 'downloads/%(title)s.%(ext)s',  # Сохраняем в папке downloads с оригинальным именем файла
    'verbose': True,
    'noplaylist': True,
    'no-cache-dir': True,
}

async def download_and_play_song(ctx, link):
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            url2 = info['url']
            # print('info:', info)
            # print('url2:', url2)
            voice_channel = await ctx.author.voice.channel.connect()
            voice_channel.play(discord.FFmpegPCMAudio(fr'downloads\{info['title']}.opus'),
                               after=lambda e: print('done', e))




        while voice_channel.is_playing():
            await asyncio.sleep(10)

        await voice_channel.disconnect()

        # Удаляем скачанный файл после проигрывания
        # os.remove(f'downloads/{info["title"]}.opus')

    except youtube_dl.DownloadError as e:
        print(f'Ошибка при скачивании контента: {e}')
    except discord.ClientException as e:
        print(f'Исключение клиента Discord: {e}')
    except Exception as e:
        print(f'Произошла ошибка: {e}')

@bot.event
async def on_ready():
    print(f'Бот подключен как {bot.user.name}')

@bot.event
async def on_message(message):
    print(f'Получено сообщение: {message}')
    print(f'Получено сообщение: {message.content}')

    await bot.process_commands(message)

@bot.command()
async def play(ctx, url):
    await download_and_play_song(ctx, url)

bot.run(config.token)
