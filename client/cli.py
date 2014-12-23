# -*- coding: utf-8 -*-

import argparse
from .commandparser import CommandParser


def init_parser():
    parser = argparse.ArgumentParser(description="NanocubeBD client")
    parser.add_argument('--port', '-p', type=int, default=5000,
                        help="Interface port")
    args = parser.parse_args()
    prompt = CommandParser(args)
    prompt.prompt = '> '
    try:
        prompt.cmdloop()
    except KeyboardInterrupt:
        prompt.do_exit(None)
