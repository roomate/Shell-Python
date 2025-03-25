# -*- coding: utf-8 -*-
"""
Created on Sat Mar 22 12:27:58 2025

@author: hugon
"""

import os
import signal
import sys

sys.path.append("/home/Projet_shell/src") #Show where files are to be fetched
os.chdir(r"/home/Projet_shell") #Change current working directory
import ls
from history import History
from parse import parse_cmds
import echo
import mkdir
import rmdir
import pwd
import man

def terminate(hist: History|None):
    #When the shell is terminated
    if hist is not None:
        hist.save('hist.pkl')
    exit(0)

DICT = {'echo': echo.echo, 'ls': ls.ls, 'mkdir': mkdir.mkdir,
        'rmdir': rmdir.rmdir, 'exit': terminate, 'pwd': pwd, 'man': man.man}

#signal.signal(signal.SIGINT, signal.SIG_IGN)

def run(cmd: str):
    """
    Call a fork. It creates both a parent and a child process that will run concurently, usually first the parent process.
    That's why a waidid is necessary.
    """
    pid = os.fork()
    if pid == 0:
        DICT[cmd[0]](cmd)
        exit(0) #Terminate the child process
    else:
        wait = os.waitid(os.P_PID, pid, os.WEXITED)
        if wait.si_code == "CLD_EXITED": #To be sure the process has exited normally, without abrupt interruption
            print("The child process has terminated with status ", wait.si_status)

def chdir(cmd: str)-> None:
    assert len(cmd) <= 2, "Too many arguments"
    try:
        os.chdir(os.path.join(os.getcwd(), cmd[1]))
    except FileNotFoundError:
        print(f"FileNotFoundError: No such file or directory: {os.path.join(os.getcwd(),cmd[1])}")

if __name__ == '__main__':
    src_folder = r"/home/Projet_shell/src"

    if os.path.exists("hist.pkl"):
        hist = History.load("hist.pkl")
    else:
        hist = History(size=0, history=[])

    #Get all the commands the bash can run
    scripts = set(filter(lambda x: x.endswith(".py"), os.listdir(src_folder)))
    while True:
        # cmd = input()

        cmd = "man ls"
        hist.append(cmd)

        noOfCommand, cmd = parse_cmds(cmd)
        for i in range(noOfCommand):
            current_cmd = cmd[i]

            if current_cmd[0] == 'exit':
                terminate(hist)
            if (current_cmd[0] + ".py") in scripts:
                run(current_cmd) #Launch command as python script
            elif current_cmd[0] == "cd":
                chdir(current_cmd)
            else:
                print(f"{current_cmd[0]}: command not found")
                terminate(None)
        break