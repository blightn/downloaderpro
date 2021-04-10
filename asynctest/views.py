from django.http import HttpResponse

import asyncio
import os
from django.conf import settings

import requests
from asgiref.sync import sync_to_async

import aiohttp
import aiofiles



files_for_downloading = (
    'https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt', # 4.04 MB - 4.2 MB (4,234,901 bytes)
    'https://raw.githubusercontent.com/zacanger/profane-words/master/words.json',  # 37.6 KB - 38.5 kB (38,477 bytes)
    'https://raw.githubusercontent.com/filiph/english_words/master/pubspec.yaml',  # 413 Bytes - 413 bytes
)

download_path = os.path.join(settings.BASE_DIR, 'downloads')


async def index(request):
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    return HttpResponse(
        '<h1 align="center">Downloader Pro</h1>'
        '<br>'
        '<p align="center"><a href="download1/">Download (requests)</a></p>'
        '<p align="center"><a href="download2/">Download (asyncio)</a></p>'
        '<p align="center"><a href="download3/">Download (gather)</a></p>'
        '<p align="center"><a href="download4/">Download (as_completed)</a></p>'
        )


async def download_async1(file_url):
    r = await sync_to_async(requests.get, thread_sensitive=True)(file_url, allow_redirects=True)

    if r.status_code != requests.codes.ok:
        raise

    file_name = file_url.split('/')[-1]
    file_path = os.path.join(download_path, file_name)

    f = open(file_path, 'wb')
    await sync_to_async(f.write, thread_sensitive=True)(r.content)

    print(f'File {file_name} was downloaded to {file_path}')

    return file_name


async def download_async2(file_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as r:
            if r.status != 200:
                raise

            data = await r.read()

    file_name = file_url.split('/')[-1]
    file_path = os.path.join(download_path, file_name)

    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(data)

    print(f'File {file_name} was downloaded to {file_path}')

    return file_name


# requests
# Ждёт завершения.
async def download1(request):
    '''
    loop = asyncio.get_event_loop()

    for url in files_for_downloading:
        loop.create_task(download_async1(url))
    '''

    for url in files_for_downloading:
        asyncio.create_task(download_async1(url))

    return HttpResponse('<h1 align="center">Downloaded</h1>')


# asyncio
# Не ждёт завершения.
async def download2(request):
    '''
    loop = asyncio.get_event_loop()

    for url in files_for_downloading:
        loop.create_task(download_async2(url))
    '''

    for url in files_for_downloading:
        asyncio.create_task(download_async2(url))

    return HttpResponse('<h1 align="center">Downloading...</h1>')


# gather
# Ждёт завершения.
async def download3(request):
    coros = [download_async2(url) for url in files_for_downloading]
    await asyncio.gather(*coros)

    return HttpResponse('<h1 align="center">Downloaded</h1>')


# as_completed
# Ждёт завершения.
async def download4(request):
    coros = [download_async2(url) for url in files_for_downloading]
    
    for future in asyncio.as_completed(coros):
        try:
            file_name = await future
            print(f'File {file_name} downloaded')
        except Exception:
            print(f'Error while downloading file {file_name}')

    return HttpResponse('<h1 align="center">Downloaded</h1>')