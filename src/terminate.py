from .history import History
import os
import signal
def terminate(hist: History|None):
    #When the shell is terminated
    signal.signal(signalnum=signal.SIGINT, handler=signal.SIG_DFL)
    if hist is not None:
        hist.save('hist.pkl')
    os.kill(os.getpid(), signal.SIGINT)