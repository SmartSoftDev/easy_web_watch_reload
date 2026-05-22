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
        print(
            f"[Async] Attempting broadcast to {len(self.connected_clients)} clients...")
        if self.connected_clients:

            tasks = [asyncio.create_task(client.send(message))
                     for client in self.connected_clients]

            await asyncio.gather(*tasks, return_exceptions=True)

            print("[Async] Manual broadcast sent successfully!")
        else:
            print("[Async] Aborted: The clients set is empty.")

    def broadcast_from_sync(self, message):
        asyncio.run_coroutine_threadsafe(
            self._async_broadcast(message),
            self.loop
        )
