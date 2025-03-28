# -*- coding: utf-8 -*-
"""
Created on Sat Mar 22 12:27:58 2025

@author: hugon
"""
import os
import signal
import src

print(src.__path__) #src has a __path__ attribute because it is a package


os.chdir("/home/Projet_shell/src")

from src.history import History
from src.parse import parse_cmds

from src.run import run, exec_command
from src.terminate import terminate
from src.signal_handler import interrupt_handler

if __name__ == '__main__':
    if os.path.exists("hist.pkl"):
        hist = History.load("hist.pkl")
    else:
        hist = History(size=0, history=[])

    #Get all the commands the bash can run
    while True:
        signal.signal(signalnum=signal.SIGTSTP, handler=signal.SIG_IGN)
        signal.signal(signalnum=signal.SIGINT, handler=signal.SIG_IGN)

        cmd = input()

        hist.append(cmd)
        noOfCommand, cmd = parse_cmds(cmd)
        for i in range(noOfCommand):
            current_cmd = cmd[i]
            if current_cmd[0] == 'exit':
                terminate(hist)
            elif current_cmd[0] == "":
                print("\n")
            else:
                exec_command(current_cmd)