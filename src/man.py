PATH_MANUAL = r"/usr/share/man"
import glob
import os

# signal.signal(signalnum=signal.SIGTSTP, handler=interrupt_handler)

def man(cmd: str):
    filename = cmd[1]
    s = glob.glob(pathname= r"man[1-8]/" + filename + ".[1-8].gz", root_dir=PATH_MANUAL)
    if s == []:
        print(f"No manual entry for {filename}")
        exit(1)
    assert len(s) == 1, "There shouldn't be more than one manual."
    manual = s[0]
    os.execvp("less", ["less", os.path.join(PATH_MANUAL, manual)])

if __name__=='__main__':
    man(["man", "less"])