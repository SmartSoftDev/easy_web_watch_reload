import subprocess
import os
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from src.utils.args import get_arguments


class FileWatcher(FileSystemEventHandler):
    def _handle_event(self, event):
        item_name = os.path.basename(event.src_path)

        print(f"Event TYPE : {event.event_type} on '{item_name}'")
        print("Running Linux command: echo hello")

        subprocess.run(['echo', 'hello'], shell=False)

    def on_created(self, event):
        self._handle_event(event)

    def on_deleted(self, event):
        self._handle_event(event)

    def on_moved(self, event):
        self._handle_event(event)


if __name__ == "__main__":
    FOLDER_TO_WATCH = "src/bin"

    args = get_arguments()

    if args.recursive:
        recursive = True
    else:
        recursive = False

    # Setup watchdog
    event_handler = FileWatcher()
    observer = Observer()
    observer.schedule(event_handler, path=FOLDER_TO_WATCH, recursive=recursive)
    observer.start()

    print("Watcher started")
    print("Press CTRL+C to exit \n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n🛑 Watcher stopped.")
    # Safely closing the thread
    observer.join()
