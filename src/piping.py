import subprocess
import sys
import os

PATH = "\home\hugon\Projects\Shell-Python\src"

def check_pipe(cmd: str):
    """
    Check if a pipe is present in the command.
    """
    if '|' in cmd:
        return True
    else:
        return False

def count_pipe(cmd: str):
    """
    Count the number of pipe present in the string cmd.
    """
    return cmd.count('|')

def pipe_cmd(cmd: str):
    n = count_pipe(cmd)
    cmd = cmd.replace(" ", "")
    cmd = cmd.split('|')
    