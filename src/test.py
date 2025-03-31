import os
import signal
import sys
import psutil

def child_process(cmd: str):
    os.setpgid(0, 0) #Call the system call setpgid() to set the process group id of the 
    #                  #process with id pid to the process group with id pgrp.

    # #Connect the background process to the terminal standard input.
    # #Similar to putting it to the foreground
    os.tcsetpgrp(sys.stdin.fileno(), os.getpid())

    #define signal handlers
    signal.signal(signalnum=signal.SIGTSTP, handler=signal.SIG_DFL)
    signal.signal(signalnum=signal.SIGINT, handler=signal.SIG_DFL)

    try:
        os.execvp(cmd[0], cmd)
    except FileNotFoundError:
        print(cmd[0] + ': command not found')
        sys.exit(1)

def parent_process2(pid: int, cmd: str):
    #Give back to this id group the control of the standard input

    #Define signal handler
    signal.signal(signalnum=signal.SIGTSTP, handler=signal.SIG_IGN)
    signal.signal(signalnum=signal.SIGINT, handler=signal.SIG_IGN)

    pid, status = os.waitpid(pid, os.WUNTRACED) #Stop waiting if child process stops or exit
    print("first", status)
    #Connect the process bact to the standard input.
    os.tcsetpgrp(sys.stdin.fileno(), os.getpid())
    pid = os.fork()
    if pid == 0:
        os.execvp("ps", ["ps"])
    else:
        os.waitid(os.P_PID, pid, os.WEXITED)

    signal.signal(signalnum=signal.SIGTTIN, handler=signal.SIG_DFL)
    signal.signal(signalnum=signal.SIGTTOU, handler=signal.SIG_DFL)

    if os.WIFEXITED(status):
        print(f"Success, the children process {pid} terminated normally.")
    elif os.WIFSTOPPED(status):
        print(f"The children process {pid} has been stopped.")
    elif status == os.CLD_KILLED:
        print(f"The children process {pid} has been killed.")

def run(cmd: str):
    """
    Call a fork to create a parent and a child process that will run concurrently.
    A waitid is implemented because you do not want the CLI to be available to the operator before the child process
    has finished.
    """
    pid = os.fork()
    if pid < 0:
        raise ValueError("Impossible to fork.")
    elif pid == 0:
        child_process(cmd)
    else:
        parent_process2(pid, cmd)

def handler(signum, frame):
    while True:
        try:
            pid, status = os.waitpid(-1, os.WNOHANG)
            print("stats", os.WIFEXITED(status))
        except ChildProcessError:
            break

if __name__ == '__main__':
    signal.signal(signalnum=signal.SIGTSTP, handler=signal.SIG_DFL)
    signal.signal(signalnum=signal.SIGINT, handler=signal.SIG_DFL)

    signal.signal(signalnum=signal.SIGTTIN, handler=signal.SIG_IGN)
    signal.signal(signalnum=signal.SIGTTOU, handler=signal.SIG_IGN)

    signal.signal(signal.SIGCHLD, handler)

    run(["sleep", "2"])
    pid = os.fork()
    if pid == 0:
        os.execvp("ps", ["ps"])
    else:
        print("what")
        os.waitid(os.P_PID, pid, os.WEXITED)
        print("bb")