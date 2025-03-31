import os
from .jobs import CHILD_BG
import signal

def child_handler(sigum, frame):
    """
    For every child process terminated, we need to make sure that it is reaped once terminated.
    The right way to do it is using a waitpid which does not block the current process. The handler is triggered every time a process
    is stopped or terminated.
    """
    # pid = os.fork()
    # signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    # if pid == 0:
    #      os.execvp('ps', ['ps'])
    # else:
    #      pass
    print("In the Handler")
    while True:
        global CHILD_BG
        try:
            pid, _ = os.waitpid(-1, os.WNOHANG)
            if pid < 0:
                print("Error, invalid process")
                return
            elif pid > 0:
                    print(pid)
                    list_id = [child.Id for child in CHILD_BG]
                    if pid in list_id:
                        CHILD_BG.pop(list_id.index(pid))
                    else:
                         break
            else:
                 break
        except ChildProcessError:
            break #No children to reap