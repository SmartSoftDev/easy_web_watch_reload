import asyncio


class FileWatcherWebSocket:
    def __init__(self, loop):
        self.connected_clients = set()
        self.loop = loop  # We must store the main async loop

    async def handler(self, websocket):
        self.connected_clients.add(websocket)
        try:
            # Keep the connection open indefinitely
            await websocket.wait_closed()
        finally:
            self.connected_clients.remove(websocket)

    async def _async_broadcast(self, message):
        if self.connected_clients:

            tasks = [asyncio.create_task(client.send(message))
                     for client in self.connected_clients]
            # concurrently runs tasks
            await asyncio.gather(*tasks, return_exceptions=True)

        else:
            print("[Async] Aborted: The clients set is empty.")

    def broadcast_from_sync(self, message):
        # is called from the synchronous file watcher, so we need to schedule the async broadcast on the main loop
        asyncio.run_coroutine_threadsafe(
            self._async_broadcast(message),
            self.loop
        )
