from pipes import quote
import io
import os

stdout = io.open(1, "wb")


def print_binary(data):
    if not isinstance(data, bytes):
        data = data.encode("utf8")
    stdout.write(data)
    stdout.flush()


def set_term_title(title):
    term = os.environ.get("TERM")
    if not isinstance(title, bytes):
        title = title.encode("utf8")
    if term.startswith("xterm"):
        print_binary(b"\x1B]0;%s\x07" % title)
    if term in ["screen"]:
        print_binary(b"\033k%s\033\\" % title)


def get_file_size(path):
    return os.stat(path).st_size


def edit_file(file_):
    editors = [
        os.getenv("EDITOR", "xdg-open"), "xdg-open", "open", "subl", "vim",
        "vi", "nano", "pico"]
    for editor in editors:
        if not os.system("{0} {1}".format(editor, quote(file_))):
            return 0
