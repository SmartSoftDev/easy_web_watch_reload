import asyncio
import os
import sys

from websockets.asyncio.server import serve
from watchdog.observers import Observer
from src.bin.lib.server.watcher_websocket import FileWatcherWebSocket
from src.bin.lib.watching import FileWatcher
from src.bin.lib.args import get_arguments
# from websockets.asyncio.server import serve


async def main():

    args = get_arguments()
    port = args.port
    watcher_path = os.path.abspath(args.watch_path)
    html_generator_path = os.path.abspath(args.html_generator_path)
    config_path = os.path.abspath(args.config_path)

    if not os.path.exists(watcher_path):
        print(f"❌ Error: The directory '{watcher_path}' does not exist!")
        sys.exit(1)
    print(f"Watching path: {watcher_path} (recursive: {args.recursive})")
    if args.recursive:
        recursive = True
    else:
        recursive = False

    # loop reference to bridge the gap between the synchronous file watcher and the asynchronous WebSocket server
    loop = asyncio.get_running_loop()
    ws_server = FileWatcherWebSocket(loop)
    event_handler = FileWatcher(ws_server, html_generator_path, config_path)

    # Set up the file system observer to watch for changes in the specified directory
    observer = Observer()
    observer.schedule(
        event_handler, path=f"{watcher_path}", recursive=recursive)
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
