from aiohttp import web


async def json(data, status=200, headers=None):
    response = web.json_response(data, status=status, headers=headers, content_type='application/json')
    return response


async def raw_json(data, status=200, headers=None):
    response = web.Response(text=data, status=status, headers=headers, content_type='application/json')
    return response


async def raw(data, status=200, headers=None):
    response = web.Response(text=data, status=status, headers=headers, content_type='text/plain')
    return response


async def stream():
    return web.StreamResponse(
        status=200,
        reason='OK',
        headers={'Content-Type': 'text/plain'},
    )
