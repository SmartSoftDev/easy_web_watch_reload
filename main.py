import asyncio
from watchdog.observers import Observer
from src.server.watcher_websocket import FileWatcherWebSocket
from src.bin.watcher import FileWatcher
from src.utils.args import get_arguments
from websockets.asyncio.server import serve


async def main():
    loop = asyncio.get_running_loop()

    ws_server = FileWatcherWebSocket(loop)
    event_handler = FileWatcher(ws_server)

    args = get_arguments()

    if args.recursive:
        recursive = True
    else:
        recursive = False

    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=recursive)
    observer.start()

    async with serve(ws_server.handler, "localhost", 8765):
        print("Server listening... Modify a file in this directory!")

        try:
            await asyncio.Future()
        except KeyboardInterrupt, asyncio.CancelledError:
            observer.stop()

    observer.join()

if __name__ == "__main__":
    asyncio.run(main())
