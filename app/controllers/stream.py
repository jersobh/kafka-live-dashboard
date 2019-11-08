import asyncio
import json
import random

import aiohttp
import motor.motor_asyncio
from aiohttp import web
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

loop = asyncio.get_event_loop()
client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://mongodb:27017')
db = client['kafka_data']
clients = []


async def send_msg():
    producer = AIOKafkaProducer(
        loop=loop, bootstrap_servers=['kafka1:9092', 'kafka2:9093', 'kafka3:9094'])
    await producer.start()
    try:
        # Produce message
        sale_value = round(random.uniform(1.5, 99.99), 2)
        random_message = json.dumps({'type': 'sale', 'value': sale_value})
        await producer.send_and_wait("iot_messages", random_message.encode('utf-8'))
    finally:
        await producer.stop()


async def receive_msg():
    consumer = AIOKafkaConsumer(
        'iot_messages',
        loop=loop, bootstrap_servers=['kafka1:9092', 'kafka2:9093', 'kafka3:9094'])
    await consumer.start()
    try:
        msg = await consumer.getone()
        return {'msg': msg.value.decode('utf-8'), 'time': msg.timestamp}
    finally:
        await consumer.stop()


async def produce():
    try:
        while True:
            await asyncio.sleep(5)
            await send_msg()
    except asyncio.CancelledError:
        print('Cancel consumer: close connections')
        pass


async def consume():
    try:
        while True:
            await asyncio.sleep(5)
            data = await receive_msg()
            for ws in clients:
                await ws.send_str(json.dumps(data))
            await db.kafka.insert_one(data)
    except asyncio.CancelledError:
        print('Cancel consumer: close connections')
        pass


async def ws_handler(request):
    ws = aiohttp.web.WebSocketResponse()
    await ws.prepare(request)
    if ws not in clients:
        clients.append(ws)
    try:
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                    clients.remove(ws)
            elif msg.type == aiohttp.WSMsgType.CLOSED:
                break
            elif msg.type == aiohttp.WSMsgType.ERROR:
                break
    except asyncio.CancelledError:
        clients.remove(ws)
    finally:
        clients.remove(ws)
        await ws.close()
    return ws
