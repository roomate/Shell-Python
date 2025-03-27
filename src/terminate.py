from history import History
def terminate(hist: History|None):
    #When the shell is terminated
    if hist is not None:
        hist.save('hist.pkl')
    exit(0)