import asyncio
import websockets
from threading import Thread
from time import sleep

class FrontServer:
    def __inti__(self):
        self.name = "front server"
        self.thread = None
        self.websocket = websockets.serve(self._onMessge, "localhost", 8765)

    async def _onMessge(self, websocket, path):
        async for message in websocket:
            await websocket.send(message + " returning msg back")
            print(f"message = {message}")

    def _isUp(self):
        return True

    def _waitStarUp(self):
        while not self._isUp():
            continue

    def _initServer(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.websocket)
        loop.run_forever()

    def runServer(self):
        self.thread = Thread(target=self._initServer)
        self.thread.start()
        self._waitStarUp()

frontServer = FrontServer()
frontServer.runServer()

print("got here")
while True:
    sleep(1)
    print("running main thread")

# https://www.youtube.com/watch?v=lv0oEnQY1pM&ab_channel=Vuka
# https://websockets.readthedocs.io/en/stable/index.html