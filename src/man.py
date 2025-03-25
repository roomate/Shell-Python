PATH_MANUAL = r"/usr/share/man"
import glob
import gzip
import os
import signal
import time

def terminate_handler(signal, frame):
    print("You're terminating the process.")
    exit(0)

signal.signal(signal.SIGINT, handler=terminate_handler)

def interrupt_handler(signum, frame):
        """
        Handler to put a the current process in the background. NOTE: It does NOT pause the process.
        """
        print("You put the current process in the background.")
        signal.signal(signum, signal.SIG_DFL) #Define the handler
        signal.raise_signal(signal.SIGSTOP) #Call the handler

# Note: if you do NOT declare a handler in the above function with signal.signal, then raise signal will call the last
#declared handler, which is the function itself. Hence, it enters in an infinite recursive loop!

signal.signal(signal.SIGTSTP, interrupt_handler)

def man(cmd: str):
    filename = cmd[1]
    s = glob.glob(pathname= r"man[1-8]/" + filename + ".[1-8].gz", root_dir=PATH_MANUAL)
    if s == []:
        print(f"No manual entry for {filename}")
        exit(1)
    assert len(s) == 1, "There shouldn't be more than one manual."
    manual = s[0]
    with gzip.open(filename=os.path.join(PATH_MANUAL, manual), mode='rt', encoding = 'utf-8') as file:
        content = file.read()
    print(content)
    exit(0)
