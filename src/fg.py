import signal

def fg(cmd: str):
    signal.signal(signalnum=signal.SIGCONT, handler=signal.SIG_DFL)
    signal.raise_signal(signal.SIGCONT)