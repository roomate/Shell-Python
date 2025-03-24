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
from parse_cmd import parse_cmd
from echo import echo

#signal.signal(signal.SIGINT, signal.SIG_IGN)

def run(cmd: str):
    PATH = r"/home/Projet_shell/src/"
    pid = os.fork()
    if pid == 0:
        if cmd[0] == 'ls':
            ls.ls(cmd)
        elif cmd[0] == 'mkdir':
            pass
        elif cmd[0] == "echo":
            echo.echo(cmd)
        exit(0)
    else:
        wait = os.waitid(os.P_PID, pid, os.WEXITED)
        if wait.si_code == "CLD_EXITED": #To be sure the process has exited normally, without abrupt interruption
            print("The child process has terminated with status ", wait.si_status)


if __name__ == '__main__':
    os.environ["PATH_SHELL"] = r"/home/Projet_shell/src"

    if os.path.exists("hist.pkl"):
        hist = History.load("hist.pkl")
    else:
        hist = History(size=0, history=[])

    #Get all the commands the bash can run
    scripts = list(filter(lambda x: x.endswith(".py"), os.listdir(os.environ["PATH_SHELL"])))
    while True:
        # cmd = input()
        cmd = "echo"
        hist.append(cmd)

        noOfCommand, cmd = parse_cmd(cmd)
        for i in range(noOfCommand):
            current_cmd = cmd[i]

            if (current_cmd[0] + ".py") in scripts:
                run(current_cmd) #Launch command as python script

            elif current_cmd[0] == "cd":
                assert len(current_cmd) <= 2, "too many arguments"
                os.chdir(current_cmd[1])
            else:
                #When the shell is terminated
                print("break")
                hist.save('hist.pkl')
                break
        break