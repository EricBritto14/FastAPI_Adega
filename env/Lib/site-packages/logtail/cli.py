import sys
import argparse
import time
from .utils import edit_file
from .logtail import LogTailer


class ArgumentParser(argparse.ArgumentParser):
    def __init__(self):
        usage_string = "logtail <folder> [<glob>]"
        super(ArgumentParser, self).__init__(
            usage=usage_string, description="Log tailer")

        self.prog = "Argument Parser"

        self.add_argument(
            "folder", default=".", action="store",
            nargs="?", help="Folder to search in")

        self.add_argument(
            "-g", "--glob", default="*", action="store",
            help="Globbing file match express")


def entry_point():
    args = ArgumentParser().parse_args()
    logtail = LogTailer(args.folder, args.glob)
    if sys.argv[0].endswith("editlatest"):
        edit_file(logtail.get_last_changed())
    else:
        while True:
            logtail.print_latest()
            time.sleep(.1)
