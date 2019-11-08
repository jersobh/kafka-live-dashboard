import aiohttp_cors

from controllers import main, stream


def routes(app):
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })
    cors.add(app.router.add_get('/', main.index))
    cors.add(app.router.add_get('/ws', stream.ws_handler))
    cors.add(app.router.add_get('/get-orders/', main.watch))
