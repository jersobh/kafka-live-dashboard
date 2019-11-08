import asyncio

import aiohttp_jinja2
import jinja2
from aiohttp import web

from controllers import stream
from core.router import routes


async def start_background_tasks(app):
    app['stream_producer'] = asyncio.ensure_future(stream.produce())
    app['stream_consumer'] = asyncio.ensure_future(stream.consume())


async def cleanup_background_tasks(app):
    app['stream_producer'].cancel()
    await app['stream_producer']
    app['stream_consumer'].cancel()
    await app['stream_consumer']


async def factory():
    loop = asyncio.get_event_loop()
    app = web.Application(loop=loop)
    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader('views/templates/'))
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    routes(app)
    return app
    # web.run_app(app, host='0.0.0.0', port=APP_PORT)
