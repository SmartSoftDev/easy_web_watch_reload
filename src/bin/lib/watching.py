import subprocess
import os
import json

from watchdog.events import FileSystemEventHandler

from src.bin.lib.server.html_injector import inject_websocket_client


class FileWatcher(FileSystemEventHandler):
    def __init__(self, ws_server, html_generator_path, config_path):
        super().__init__()

        self.ws_server = ws_server
        self.html_generator_path = html_generator_path
        self.config_path = config_path

    def _get_item_name(self, event):
        return os.path.basename(event.src_path)

    def _broadcast_event(self, event_type, item_name):
        event_data = {
            "type": event_type,
            "item": item_name,
        }
        json_message = json.dumps(event_data)

        # bridging synchronous file watcher with asynchronous WebSocket server
        self.ws_server.broadcast_from_sync(json_message)

        subprocess.run(['python3', self.html_generator_path, '--project-config',
                       self.config_path, '--html'], shell=False)

        server_port = self.ws_server.server.sockets[0].getsockname()[1]
        inject_websocket_client(server_port)

    def on_created(self, event):
        self._broadcast_event("on_created", self._get_item_name(event))

    def on_deleted(self, event):
        self._broadcast_event("on_deleted", self._get_item_name(event))

    def on_moved(self, event):
        self._broadcast_event("on_moved", self._get_item_name(event))

    def on_modified(self, event):
        self._broadcast_event("on_modified", self._get_item_name(event))
