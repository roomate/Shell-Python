from src.run import scripts, DICT, parent_process
import os
import signal
import sys
from src.jobs import jobs, CHILD_BG, Jobs

flags = os.WEXITED | os.WSTOPPED

PATH = r"\home\hugon\Projects\Shell-Python\src"

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

def pipe_cmd(cmds: str):

    cmds = cmds.split('|')
    o_fd, i_fd = os.pipe()
    #First command
    cmds[0] = cmds[0].strip()
    cmd = cmds[0].split()
    pid = os.fork()
    if pid == 0:
        os.setpgid(0, 0) #Call the system call setpgid() to set the process group id of the 
                        #process with id pid to the process group with id pgrp.
        os.dup2(i_fd, sys.stdout.fileno())
        
        #Connect the background/child process to pipe output.
        #Similar to putting it to the foreground
        os.tcsetpgrp(sys.stdin.fileno(), os.getpid())

        # #Activate signal handlers to default mode
        signal.signal(signalnum=signal.SIGTSTP, handler=signal.SIG_DFL)
        signal.signal(signalnum=signal.SIGINT, handler=signal.SIG_DFL)
        try:
            os.execvp(cmd[0], cmd)
        except FileNotFoundError:
            print(cmd + ': command not found')
            sys.exit(1)
    elif pid > 0:
        parent_process(pid, cmd)

    for cmd in cmds[1:-1]:
        cmd = cmd.split(" ")
        cmd = cmd.strip()
        pid = os.fork()
        if pid == 0:
            os.setpgid(0, 0) #Call the system call setpgid() to set the process group id of the 
                        #process with id pid to the process group with id pgrp.
            os.dup2(o_fd, sys.stdin.fileno())
            os.dup2(i_fd, sys.stdout.fileno())

            #define signal handlers
            signal.signal(signalnum=signal.SIGTSTP, handler=signal.SIG_DFL)
            signal.signal(signalnum=signal.SIGINT, handler=signal.SIG_DFL)
            try:
                os.execvp(cmd[0], cmd)
            except FileNotFoundError:
                print(cmd[0] + ': command not found')
                sys.exit(1)
        elif pid > 0:
            parent_process(pid, cmd)

    #Last command
    cmd = cmds[-1].strip()
    cmd = cmd.split(" ")
    pid = os.fork()
    if pid == 0:
        os.setpgid(0, 0) #Call the system call setpgid() to set the process group id of the 
                        #process with id pid to the process group with id pgrp.
        os.dup2(o_fd, sys.stdin.fileno())

        #Activate signal handlers to default mode
        signal.signal(signalnum=signal.SIGTSTP, handler=signal.SIG_DFL)
        signal.signal(signalnum=signal.SIGINT, handler=signal.SIG_DFL)
        try:
            os.execvp(cmd[0], cmd)
        except FileNotFoundError:
            print(cmd + ': command not found')
            sys.exit(1)
    elif pid > 0:
        parent_process(pid, cmd)