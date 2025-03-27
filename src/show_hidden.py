import ctypes
import os
from collections.abc import Callable

os.chdir("/home/Projet_shell")

def hidden_files(directory: str, Callback_file: Callable = lambda *args: None, Callback_dir: Callable = print):
    for dirpath, dirname, filename in os.walk(directory):
        for file in filename:
            if file.startswith("."):
                Callback_file(os.path.join(dirpath, file))
        for dir_ in dirname:
            if dir_.startswith("."):
                Callback_dir(os.path.join(dirpath, dir_))

hidden_files(os.getcwd(), Callback_dir=print)