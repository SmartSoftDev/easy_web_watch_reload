import asyncio

from watchdog.observers import Observer
from src.server.watcher_websocket import FileWatcherWebSocket
from src.bin.watcher import FileWatcher
from src.utils.args import get_arguments
from websockets.asyncio.server import serve


async def main():
    # loop reference to bridge the gap between the synchronous file watcher and the asynchronous WebSocket server
    loop = asyncio.get_running_loop()

    ws_server = FileWatcherWebSocket(loop)
    event_handler = FileWatcher(ws_server)

    args = get_arguments()
    port = args.port
    watcher_path = args.watch_path
    print(f"Watching path: {watcher_path} (recursive: {args.recursive})")
    if args.recursive:
        recursive = True
    else:
        recursive = False    

    observer = Observer()
    observer.schedule(event_handler, path=f"../{watcher_path}", recursive=recursive)
    observer.start()

    async with serve(ws_server.handler, "localhost", port) as server:
        print("Server listening... Modify a file in this directory!")
        ws_server.server = server
        try:
            # keep the server running indefinitely, until interrupted
            await asyncio.Future()
        except KeyboardInterrupt, asyncio.CancelledError:
            observer.stop()
    # safely stop the observer thread and wait for it to finish
    observer.join()

if __name__ == "__main__":
    asyncio.run(main())
