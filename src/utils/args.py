import argparse


def get_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        help="If included, watches all subfolders inside the target path."
    )
    parser.add_argument(
        "-p", "--port",
        type=int, default=8765,
        help="Port number for the WebSocket server (default: 8765)"
    )
    parser.add_argument(
        "-watch", "--watch-path",
        type=str, default="Core/ssd/iotp/whmi/reqs",
        help="Path to the directory to watch for changes (default: Core/ssd/iotp/whmi/reqs)"
    )
    return parser.parse_args()
