#!/usr/bin/env python
import argparse
import os
import sys

# Import muthur_gpt
muthur_lib = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
if muthur_lib not in sys.path:
    sys.path.append(muthur_lib)
from muthur_gpt import controller


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--debug", action="store_true",
        help="Run in debug mode to use local testing rather than chatGPT. "
        "Be aware debug can also be specified in the config. If debug mode "
        "via either means, then muthur will run in debug mode.")
    parser.add_argument(
        "--plugin", default="cronus", dest="plugin_name",
        help="Specify a particular Muthur plugin. Defaults to Cronus. Will be ignored if --save is specified")
    parser.add_argument(
        "--mute", action="store_true",
        help="Run with no sound.")
    parser.add_argument(
        "--api-key", help="Specify an openAI API key. Can also be supplied via "
        "config or environment variable. Envvar is preferred.")
    parser.add_argument(
        "--save", default=None, dest="save_file",
        help="Specify save file name to be loaded")
    return parser.parse_args()


def main():
    args = parse_args()
    muthur_controller = controller.MuthurController.create_from_args(args)
    muthur_controller.run()


if __name__ == "__main__":
    main()
