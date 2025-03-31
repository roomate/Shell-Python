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
from src.jobs import jobs, CHILD_BG, Jobs
from src.pid import pid

src_folder = r"/home/hugon/Projects/Shell-Python/src"
scripts = set(filter(lambda x: x.endswith(".py"), os.listdir(src_folder)))
DICT = {'echo': echo, 'ls': ls, 'mkdir': mkdir,
        'rmdir': rmdir, 'exit': terminate, 'pwd': pwd, 'man': man,
        'bg': bg, 'cd': chdir, 'jobs': jobs, 'pid': pid}

#Should be similar to os.WUNTRACED
flags = os.WEXITED | os.WSTOPPED

def child_process(cmd: str):
    """
    The child process is automatically terminated after execution according to POSIX documentation.
        - setpgid(0,0): create a new group of process whose leader is the calling process, that is the child process.
        - tcsetpgrp(fildes, pid): connect the process whose id is pid to the controlling terminal..
    """
    os.setpgid(0, 0) #Call the system call setpgid() to set the process group id of the 
                     #process with id pid to the process group with id pgrp.

    #Connect the background process to the terminal standard input.
    #Similar to putting it to the foreground
    os.tcsetpgrp(sys.stdin.fileno(), os.getpid())

    #define signal handlers
    signal.signal(signalnum=signal.SIGTSTP, handler=signal.SIG_DFL)
    signal.signal(signalnum=signal.SIGINT, handler=signal.SIG_DFL)

    try:
        os.execvp(cmd[0], cmd)
    except FileNotFoundError:
        print(cmd[0] + ': command not found')
        sys.exit(1)

def parent_process(pid: int, cmd: str):
    # print(f"In parent process, Id is {os.getpid()}")
    wait = os.waitid(os.P_PID, pid, flags) #Stop waiting if child process stops or exit

    #Connect the process bact to the standard input.
    os.tcsetpgrp(sys.stdin.fileno(), os.getpid())

    signal.signal(signalnum=signal.SIGTTIN, handler=signal.SIG_DFL)
    signal.signal(signalnum=signal.SIGTTOU, handler=signal.SIG_DFL)

    if wait.si_code == os.CLD_EXITED:
        print(f"Success, the children process {pid} terminated normally.")
    elif wait.si_code == os.CLD_STOPPED:
        print(f"The children process {pid} has been stopped.")
        J = Jobs(name=cmd[0], Id=pid, status=0, index=len(CHILD_BG))
        CHILD_BG.append(J) #Add the new background process in the CHILD_PS list
    elif wait.si_code == os.CLD_KILLED:
        print(f"The children process {pid} has been killed.")

def run(cmd: str):
    """
    Call a fork to create a parent and a child process that will run concurrently.
    A waitid is implemented because you do not want the CLI to be available to the operator before the child process
    has finished.

    NOTE:
    If a background process tries to read or write the terminal, then 
    it receives respectively a signal SIGTTOU or SIGTTIN, having the immediate effect to pause it.
    Ignoring those signals is necessary if we want to use tcsetpgrp. If you do not, then it pauses the child process
    when reading tcsetpgrp.
    """
    signal.signal(signalnum=signal.SIGTTIN, handler=signal.SIG_IGN)
    signal.signal(signalnum=signal.SIGTTOU, handler=signal.SIG_IGN)
    pid = os.fork()
    if pid < 0:
        raise ValueError("Impossible to fork.")
    elif pid == 0:
        child_process(cmd)
    else:
        parent_process(pid, cmd)

def run_builtin(cmd: str):
    """
    Note: 
    Since we do not use execvp here, the child process is not replaced by a subshell (see execvp doc) and terminated.
    That is why the exit(0) command is necessary here.
    """
    signal.signal(signalnum=signal.SIGTTIN, handler=signal.SIG_IGN)
    signal.signal(signalnum=signal.SIGTTOU, handler=signal.SIG_IGN)
    pid = os.fork()
    if pid < 0:
        print("Unable to fork process")
    elif pid == 0:
        os.setpgid(0,0)
        os.tcsetpgrp(sys.stdin.fileno(), os.getpid())
        #define signal handlers
        signal.signal(signalnum=signal.SIGTSTP, handler=signal.SIG_DFL)
        signal.signal(signalnum=signal.SIGINT, handler=signal.SIG_DFL)
        DICT[cmd[0]](cmd) #Launch builtin method
        exit(0)
    else:
        wait = os.waitid(os.P_PID, pid, flags)
        # Connect the process bact to the standard input.
        os.tcsetpgrp(sys.stdin.fileno(), os.getpid())

        signal.signal(signalnum=signal.SIGTTIN, handler=signal.SIG_DFL)
        signal.signal(signalnum=signal.SIGTTOU, handler=signal.SIG_DFL)
        if wait.si_code == os.CLD_EXITED:
            print(f"Success, the children process {pid} terminated normally.")
        elif wait.si_code == os.CLD_STOPPED:
            print(f"The children process {pid} has been stopped.")
            J = Jobs(name=cmd[0], Id=pid, status=0, index=len(CHILD_BG))
            CHILD_BG.append(J) #Add the new background process in the CHILD_PS list
        elif wait.si_code == os.CLD_KILLED:
            print(f"The children process {pid} has been killed.")

def exec_command(cmd: str):
    """
    Putting a process in the background can be complex, because we have to deal with multithreading, and it implies
    dealing with signal, whose behaviour can be tricky to grasp.
    """
    if (cmd[0] + ".py") in scripts:
        run_builtin(cmd)
    else:
        run(cmd)