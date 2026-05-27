import asyncio

from Core.devices.rpi.picow.ghempy import schedule


class FileWatcherWebSocket:
    def __init__(self, loop):
        self.connected_clients = set()
        # storing specific event loop reference allows
        # to schedule asynchronous tasks from synchronous code
        self.loop = loop

    async def handler(self, websocket):
        self.connected_clients.add(websocket)
        try:
            # Keep the connection open indefinitely
            await websocket.wait_closed()
        finally:
            self.connected_clients.remove(websocket)

    async def _async_broadcast(self, message):
        if self.connected_clients:
            # asynchronously schedules coroutines in event loop
            tasks = [asyncio.create_task(client.send(message))
                     for client in self.connected_clients]
            # concurrently runs tasks
            await asyncio.gather(*tasks, return_exceptions=True)

        else:
            print("Aborted: The clients set is empty.")

    def broadcast_from_sync(self, message):
        # schedule the async broadcast on the asyncio event loop
        asyncio.run_coroutine_threadsafe(
            self._async_broadcast(message),
            self.loop
        )
