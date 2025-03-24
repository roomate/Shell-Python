# -*- coding: utf-8 -*-
"""
Created on Sat Mar 22 17:12:53 2025

@author: hugon
"""

import os
import time
import typing
from collections.abc import Callable

#Color metadata
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def ListFile(d: str, param: dict):
    if not param["show_inode"]:
        if os.path.isfile(d):
            print(d, end = " ")
        elif os.path.isdir(d):
            print(bcolors.OKBLUE + bcolors.BOLD + d + bcolors.ENDC, end=" ")
    else:
        inode = os.stat(d).st_ino
        if os.path.isfile(d):
            print(inode, d, end = " ")
        elif os.path.isdir(d):
            print(str(inode) + " " + bcolors.OKBLUE + bcolors.BOLD + d + bcolors.ENDC, end=" ")


def ListDir(directory: str, Callback: Callable = ListFile, param: dict = {}):


    assert directory is not None, "Directory should not be None"
    assert callable(Callback), "Callback should be callable"
    assert param != {}, "Flags should not be empty"

    files = os.listdir(directory)#Get all files and directories
    for file in files:
        if not param["show_hidden"] and file.startswith("."):
            continue
        else:
            Callback(file, param)
    print()

def ls(cmd: list[str]|None = None):
    """
    Exec ls command. cmd is a list of string that should contains the command to execute ('ls' here), followed by
    directory investigated and optional flags.

    There is four cases to consider in the prompt.
    1. No flag or directory; easily checked
    2. No directory, but with flags; just set the directory as the cwd
    3. No flags, but with directory; just set the path and print.
    4. Flags and a directory; same as 2., the only difference being the path.
    """
    param = {}
    param['show_hidden']= False
    param["show_inode"]= False
    flags = cmd[1:]

    #If there is no flags or directory
    if flags == []:
        path = os.getcwd()
        ListDir(directory=path, param=param)
        exit(0)

    #If there is no directory
    if flags[0].startswith("-"):
        path = os.getcwd()
    else:
    #If there is a directory
        path = os.path.abspath(flag[0]) #Get the absolute normalized path
        #Check this is an actual directory
        if not os.path.exists(path):
            print(f'ls: cannot access {os.path.basename(path)}: No such file or directory')
            exit(1)
        flags = flags[1:]
        #If there is a directory but no flag
        if flags == []:
            ListDir(directory=path, param=param)
            exit(0)

    #Check all flags starts with a - or --
    check_flag = filter(lambda x: x.startswith("-") or x.startswith("--"), flags)
    assert False not in check_flag, "error, unsupported syntax"

    if '-a' in flags or "--all" in flags: #je rajout cacou ici
        param["show_hidden"] = True

    if '-i' in flags or '--inode' in flags:
        param["show_inode"] = True

    ListDir(directory=path, param=param)
    exit(0)