import signal
import sys
import os
from src.jobs import CHILD_BG
import psutil

flags = os.WEXITED | os.WSTOPPED

def fg(cmd: str):
    """
    This process can not be run a child process because it needs access to the child processes of the 
    calling process.
    """
    global CHILD_BG
    assert len(cmd) >= 1, ValueError("not enough arguments.")
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    signal.signal(signal.SIGTSTP, signal.SIG_DFL)

    signal.signal(signal.SIGTTIN, signal.SIG_IGN)
    signal.signal(signal.SIGTTOU, signal.SIG_IGN)

    current_process = psutil.Process()
    child = current_process.children(recursive=True)
    print("child are", child)

    assert len(CHILD_BG) > 0, ChildProcessError("No background process exist")

    if len(cmd) == 1:
        ps = CHILD_BG[-1].Id

        #Give the control of the terminal to the last declared background process.
        os.tcsetpgrp(sys.stdin.fileno(), ps)

        os.kill(ps, signal.SIGCONT) #Continue the process, if it was stopped

        pid, status = os.waitpid(ps, os.WUNTRACED) #Wait the process is terminated or stopped

        #Give the control of the terminal back to the calling process
        os.tcsetpgrp(sys.stdin.fileno(), os.getpid())

        #Set the signals back to their original state
        signal.signal(signal.SIGTTIN, signal.SIG_DFL)
        signal.signal(signal.SIGTTOU, signal.SIG_DFL)

        if os.WIFSTOPPED(status):
            print(f"The process {ps} has been stopped by CTRL+Z command")
        elif os.WIFEXITED(status):
            CHILD_BG.pop()
            print(f"The process {ps} terminated normally.")
        else:
            list_id = [chld.Id for chld in CHILD_BG]
            pid = cmd[1]
            if pid not in list_id:
                print("The process with id {pid} is not a background process.")
            ps = CHILD_BG[list_id.index(pid)].Id

            #Give the control of the terminal to the background process
            os.tcsetpgrp(sys.stdin.fileno(), ps)

            #Tell the process to continue
            os.kill(ps, signal.SIGCONT)

            #Wait for the process to be terminated or stopped
            pid, status = os.waitid(ps, flags)

            #set the signals back to their default mode
            signal.signal(signal.SIGTTIN, signal.SIG_DFL)
            signal.signal(signal.SIGTTOU, signal.SIG_DFL)

            #Give the control of the terminal back to the calling process
            os.tcsetpgrp(sys.stdin.fileno(), os.getpid())
            if os.WIFSTOPPED(status):
                print(f"The process {ps} has been stopped by CTRL+Z command")
            elif os.WIFEXITED(status):
                print(f"The process {ps} terminated normally.")
                CHILD_BG.drop(list_id.index(pid))