from fnmatch import fnmatch
import os
from .utils import print_binary, get_file_size, set_term_title
from collections import defaultdict


class LogTailer(object):
    def __init__(self, folder, glob="*"):
        self.file_tracker = defaultdict(int)
        self.folder = folder
        self.glob = glob
        self.register_existing_files()

    def register_existing_files(self):
        for file_ in self.get_changed_files(False):
            self.file_tracker[file_] = get_file_size(file_)

    def get_changed_files(self, print_new=True):
        current = set()
        for path, dirs, files in os.walk(self.folder):
            for f in files:
                if not fnmatch(f, self.glob):
                    continue
                file_ = os.path.realpath(os.path.expanduser(
                    os.path.join(path, f)))
                if os.path.exists(file_):
                    current.add(file_)

        for file_ in set(self.file_tracker) - current:
            print_binary(u"File removed: {0}\n".format(file_))
            self.file_tracker.pop(file_)

        for file_ in current:
            if file_ not in self.file_tracker and print_new:
                print_binary(u"New File: {0}\n".format(file_))
            size = get_file_size(file_)
            if size != self.file_tracker[file_]:
                if size < self.file_tracker[file_]:
                    print_binary(u"File Truncated: {0}\n".format(file_))
                    self.file_tracker[file_] = 0
                yield file_

    def get_last_changed(self):
        current_time = 0
        current_file = None
        for path, dirs, files in os.walk(self.folder):
            for f in files:
                if not fnmatch(f, self.glob):
                    continue
                file_path = os.path.join(path, f)
                mtime = os.stat(file_path).st_mtime
                if mtime > current_time:
                    current_time = mtime
                    current_file = file_path
        return current_file

    def print_latest(self):
        for file_ in self.get_changed_files(True):
            set_term_title(file_)
            old_size = self.file_tracker[file_]
            with open(file_, "rb") as f:
                f.seek(old_size)
                size = get_file_size(file_)
                print_binary(f.read(size - old_size))
                self.file_tracker[file_] = size
