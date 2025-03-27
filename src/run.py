import os
import echo
import mkdir
import rmdir
import pwd_shell
import man
import bg
# import fg
import ls
import cd
import terminate
from jobs import jobs
import signal
import sys

src_folder = r"/home/Projet_shell/src"
scripts = set(filter(lambda x: x.endswith(".py"), os.listdir(src_folder)))
DICT = {'echo': echo.echo, 'ls': ls.ls, 'mkdir': mkdir.mkdir,
        'rmdir': rmdir.rmdir, 'exit': terminate.terminate, 'pwd': pwd_shell.pwd, 'man': man.man,
        'bg': bg.bg, 'cd': cd.chdir, 'jobs': jobs}

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
        try:
            os.system(''.join(cmd))
            sys.exit(1)
        except FileNotFoundError:
            print(cmd[0] + ': command nott found')
            sys.exit(1)
    else:
        wait = os.waitid(os.P_PID, pid, os.WEXITED)
def exec_command(cmd: str):
    if (cmd[0] + ".py") in scripts:
        DICT[cmd[0]](cmd) #Launch command as python script
    elif cmd[0] == "cd":
        cd.chdir(cmd)
    else:
        run(cmd)

if __name__=='__main__':
    from parse import parse_cmds
    while 1:
        _, A = parse_cmds(input())
        for i in A:
            exec_command(i)