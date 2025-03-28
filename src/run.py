import os
import sys

from src.echo import echo
from src.mkdir import mkdir
from src.rmdir import rmdir
from src.pwd_shell import pwd
from src.man import man
from src.bg import bg
# import fg
from src.ls import ls
from src.cd import chdir
from src.terminate import terminate
import signal
from src.jobs import jobs, CHILD_PS, Jobs
from src.signal_handler import interrupt_handler, terminate_handler

src_folder = r"/home/Projet_shell/src"
scripts = set(filter(lambda x: x.endswith(".py"), os.listdir(src_folder)))
DICT = {'echo': echo, 'ls': ls, 'mkdir': mkdir,
        'rmdir': rmdir, 'exit': terminate, 'pwd': pwd, 'man': man,
        'bg': bg, 'cd': chdir, 'jobs': jobs}

flags = os.WSTOPPED | os.WEXITED

def child_process(cmd: str):
    os.setpgid(0, 0) #Call the system call setpgid() to set the process group id of the 
                     #process with id pid to the process group with id pgrp.

    #Connect the background process to the terminal standard input.
    os.tcsetpgrp(sys.stdin.fileno(), os.getpid())

    #define signal handler
    signal.signal(signalnum=signal.SIGTSTP, handler=signal.SIG_DFL)
    signal.signal(signalnum=signal.SIGINT, handler=signal.SIG_DFL)

    try:
        os.execvp(cmd[0], cmd)
    except FileNotFoundError:
        print(cmd[0] + ': command not found')
        sys.exit(1)

def parent_process(pid: int, cmd: str):
    #Give back to this id group the control of the standard input

    #Define signal handler
    signal.signal(signalnum=signal.SIGTSTP, handler=signal.SIG_IGN)
    signal.signal(signalnum=signal.SIGINT, handler=signal.SIG_IGN)

    wait = os.waitid(os.P_PID, pid, flags) #Stop waiting if child process stops or exit

    #Connect the process bact to the standard input.
    os.tcsetpgrp(sys.stdin.fileno(), os.getpid())
    if wait.si_code == os.CLD_EXITED:
        print(f"Success, the children process {pid} terminated normally.")
    elif wait.si_code == os.CLD_STOPPED:
        print(f"The children process {pid} has been stopped.")
        J = Jobs(name=cmd[0], Id=pid, status=0, index=CHILD_PS.qsize())
        CHILD_PS.append(J) #Add the new background process in the CHILD_PS list

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
        parent_process(pid, cmd)

def run_builtin(cmd: str):
    #Set the signal back to default
    signal.signal(signalnum=signal.SIGTSTP, handler=signal.SIG_DFL)
    signal.signal(signalnum=signal.SIGINT, handler=signal.SIG_DFL)
    DICT[cmd[0]](cmd) #Launch builtin method

def exec_command(cmd: str):
    """
    Putting a process in the background can be complex, because we have to deal with multithreading, and it implies
    dealing with signal, whose behaviour can be tricky to grasp.

    NOTE:
    If a background process tries to read or write the terminal, then 
    it receives respectively a signal SIGTTOU or SIGTTIN, having the immediate effect to pause it.
    Ignoring those signals is necessary if we want to use tcsetpgrp. If you do not, then it pauses the child process.
    """
    signal.signal(signalnum=signal.SIGTTIN, handler=signal.SIG_IGN)
    signal.signal(signalnum=signal.SIGTTOU, handler=signal.SIG_IGN)

    if (cmd[0] + ".py") in scripts:
        run_builtin(cmd)
    else:
        run(cmd)