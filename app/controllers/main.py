import asyncio

import aiohttp_jinja2

from controllers import stream
from views import render

loop = asyncio.get_event_loop()


async def index(request):
    data = "aiokafka stream producer/consumer to websocket "
    status = 200
    return await render.raw(data, status)


async def watch(request):
    request.app['stream_producer'] = asyncio.ensure_future(stream.produce())
    request.app['stream_consumer'] = asyncio.ensure_future(stream.consume())

    response = aiohttp_jinja2.render_template('index.jinja2',
                                              request,
                                              {})
    return response
