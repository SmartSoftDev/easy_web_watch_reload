import argparse


def get_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        help="If included, watches all subfolders inside the target path."
    )
    return parser.parse_args()
