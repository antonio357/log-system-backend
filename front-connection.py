import asyncio
import websockets

async def echo(websocket):
    async for message in websocket:
        await websocket.send(message + " returning msg back")

async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever


asyncio.run(main())

# https://websockets.readthedocs.io/en/stable/index.html