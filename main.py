# -*- coding: utf-8 -*-
"""
Created on Sat Mar 22 12:27:58 2025

@author: hugon
"""

import os
import signal
import sys

sys.path.append("/home/Projet_shell/src") #Show where files are to be fetched
sys.path.append("/home/Projet_shell") 

from history import History
from parse import parse_cmds

from jobs import Jobs, CHILD_PS

from run import run, exec_command
from terminate import terminate

# signal.signal(signalnum=signal.SIGINT, handler=signal.SIG_IGN)
signal.signal(signalnum=signal.SIGTSTP, handler=signal.SIG_IGN)

if __name__ == '__main__':
    if os.path.exists("hist.pkl"):
        hist = History.load("hist.pkl")
    else:
        hist = History(size=0, history=[])

    #Get all the commands the bash can run
    while True:
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