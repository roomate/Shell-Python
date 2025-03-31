from dataclasses import dataclass
import psutil

@dataclass
class Jobs:
    name: str
    Id: int = 0 #Process Id
    status: int = 0 #1 if running, 0 if paused
    index: int = 0

#List of Jobs in the background.
CHILD_BG = []
#Store the current foreground process
fg_PS = Jobs(name="None",Id=0,status=0,index=0)

def free_CHILD_BG():
    global CHILD_BG
    for ps in CHILD_BG:
        if ps.status == -1:
            CHILD_BG.remove(ps)

def jobs(cmd: str):
    flags = cmd[1:]
    status = []
    if len(CHILD_BG) == 0:
        print("No background process")
        return
    for ps in CHILD_BG:
        pid = ps.Id
        try:
            proc = psutil.Process(pid)
            if proc.status() == psutil.STATUS_RUNNING:
                ps.status = psutil.STATUS_RUNNING
                status.append("Running")
            elif proc.status() == psutil.STATUS_STOPPED:
                ps.status = psutil.STATUS_STOPPED
                status.append("Stopped")
            elif proc.status() == psutil.STATUS_ZOMBIE:
                ps.status = psutil.STATUS_ZOMBIE
                status.append("Zombie")
            elif proc.status() == psutil.STATUS_SLEEPING:
                ps.status = psutil.STATUS_SLEEPING
                status.append("Sleeping")
        except psutil.NoSuchProcess:
            status.append("Done")
            ps.status = -1

    if flags == []:
        for i, ps in enumerate(CHILD_BG):
            if i == len(CHILD_BG) - 1:
                print(f"[{ps.index + 1}]+  {status[i]}  {ps.name} \n")
            elif i == len(CHILD_BG) - 2:
                print(f"[{ps.index + 1}]-  {status[i]}  {ps.name} \n")
            else:
                print(f"[{ps.index + 1}]  {status[i]} {ps.name} \n")

    elif "-l" in flags:
        print(f"[{ps.index}] {ps.Id} {status[i]} {ps.name} \n")

    elif "-p" in flags:
        print(f"Id {ps.Id}\n")

    free_CHILD_BG()
    return