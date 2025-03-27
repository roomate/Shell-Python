import signal
import os

def bg(signum):
     """
     Resume the last paused process.
     """
     global CHILD_PS
     handler = signal.signal(signalnum=signum, handler=signal.SIG_DFL)
     child_pid = CHILD_PS.get()
     os.kill(child_pid, signal.SIGCONT)
