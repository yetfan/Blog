# -*- coding: utf-8 -*-
import logging; logging.basicConfig(level=logging.INFO)
from datetime import datetime
import asyncio, os, json, time
from aiohttp import web


async def index(request):
    return web.Response(body=b'<h1>Awesome</h1>', content_type='text/html')


async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    return srv

# 获取EventLoop
loop = asyncio.get_event_loop()
# 执行coroutine
loop.run_until_complete(init(loop))
loop.run_forever()
