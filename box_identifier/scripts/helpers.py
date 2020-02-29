import random
import string
import sys
import os


def random_hex_uppercase(string_length=10):
    letters = str(string.hexdigits).upper()
    return ''.join(random.choice(letters) for _ in range(string_length))


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("")

    return os.path.join(base_path, relative_path)
