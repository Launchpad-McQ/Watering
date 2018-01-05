import asyncio
import websockets
import json

relaycount = 16
sensorcount = 16

relayon=[False] * relaycount
sensorval= [0] * sensorcount

status={"relayon":relayon, "sensorval":sensorval}




async def handler(websocket, path):
    consumer_task = asyncio.ensure_future(consumer_handler(websocket))
    producer_task = asyncio.ensure_future(producer_handler(websocket))
    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )

    for task in pending:
        task.cancel()

async def consumer_handler(websocket):
    async for message in websocket:
        await consumer(message)

async def producer_handler(websocket):
    while True:
        message = await producer()
        await websocket.send(message)
        await asyncio.sleep(0.1)

async def consumer(message):
    global status
    status["relayon"][int(message)] = not status["relayon"][int(message)]
    print(message)

async def producer():
    global status
    message = json.dumps(status)
#    now = datetime.datetime.utcnow().isoformat() + 'Z'
    return message

start_server = websockets.serve(handler, '127.0.0.1', 9998)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
