import subprocess
import os
import json

from watchdog.events import FileSystemEventHandler


class FileWatcher(FileSystemEventHandler):
    def __init__(self, ws_server):
        super().__init__()

        self.ws_server = ws_server
    # def _get_path_to_run_shell_command(self,event):
    #     current_dir = os.path.dirname(os.path.abspath(__file__))
    #     shell_command_path = os.path.join(current_dir,"feat-reqs-tcs-as-code", "bin", "src", "gen_reqs.py")
    #     return shell_command_path

    def _get_item_name(self, event):
        return os.path.basename(event.src_path)

    def _broadcast_event(self, event_type, item_name):
        event_data = {
            "type": event_type,
            "item": item_name,
        }
        json_message = json.dumps(event_data)
        three_dirs_back = "../../../.."
        shell_command_path = os.path.abspath(os.path.join(__file__,three_dirs_back, "feat-reqs-tcs-as-code","src", "bin", "gen_reqs.py"))
        project_config_path = os.path.abspath(os.path.join(__file__,three_dirs_back, "feat-reqs-tcs-as-code","examples", "Project1", "config.frtac.yml"))
        self.ws_server.broadcast_from_sync(json_message)
        print(f'subprocess shouldrun on  path{shell_command_path}')
        subprocess.run(['python3', shell_command_path,'--project-config', project_config_path,'--html'], shell=False)

    def on_created(self, event):
        self._broadcast_event("on_created", self._get_item_name(event))

    def on_deleted(self, event):
        self._broadcast_event("on_deleted", self._get_item_name(event))

    def on_moved(self, event):
        self._broadcast_event("on_moved", self._get_item_name(event))
