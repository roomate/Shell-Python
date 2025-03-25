import signal

def bg(cmd: str):
    signal.signal(signalnum=signal.SIGSTOP, handler=signal.SIG_DFL)
    signal.raise_signal(signal.SIGSTOP)