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
        type=str,
        help="Path to the directory to watch for changes "
    )
    parser.add_argument(
        "--html-generator-path",
        type=str,
        help="Path to the directory which contains the HTML generator script example (gen_reqs.py) "
    )
    parser.add_argument(
        "--config-path",
        type=str,
        help="Path to the directory which contains the HTML generator config file example (config.frtac.yml) "
    )
    return parser.parse_args()
