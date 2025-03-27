import os
import signal
from jobs import Jobs, CHILD_PS

def terminate_handler(signal, frame):
    """
    Terminate a process. It is called when the operator type CTRL+C on its keyboard.
    """
    print("You're terminating the process.")
    exit(0)

def interrupt_handler(signum, frame):
        """
        Handler to put a the current process in the background AND pausing it. It is called when the operator
        type CTRL+Z on its keyboard.
        """
        print("You put the current process in the background.")
        pid = os.fork()
        if pid < 0:
             raise ValueError("Unable to fork.")
        elif pid == 0:
            signal.signal(signum, signal.SIG_DFL) #Define the handler
            signal.raise_signal(signal.SIGSTOP) #Call the newly defined handler, and stop the child process
        else:
             Jobs_bg = Jobs(id=pid, status=1, index=CHILD_PS.qsize(), name=frame.f_back.f_globals['__name__']) #The Child process' name is the name of the script 
             #triggered.
             CHILD_PS.put(Jobs_bg)
             print("pause success")
             #Register the ID of the child process
# Note: if you do NOT declare a new handler in the above function with signal.signal, then raise signal will call the last
#declared handler, which is the function itself. Hence, it enters in an infinite number of recursive loop!


if __name__ == '__main__':
    signal.signal(signalnum=signal.SIGTSTP, handler=interrupt_handler)
    import time
    while True:
        if CHILD_PS.qsize() == 1:
            exit(0)