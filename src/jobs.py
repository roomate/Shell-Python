import queue
from dataclasses import dataclass

@dataclass
class Jobs:
    name: str
    Id: int = 0
    status: int = 0 #1 if running, 0 if paused
    index: int = 0

#Objects stored are Jobs type
CHILD_PS = queue.Queue()
#Store the current foreground process
fg_PS = Jobs(name="None",Id=0,status=0,index=0)

def jobs(cmd: str):
    flags = cmd[1:]
    status = []
    for ps in CHILD_PS:
        if ps.status == 1:
            status.append("Running")
        elif ps.status == 0:
            status.append("Stopped")

    if flags == []:
        for i, ps in enumerate(CHILD_PS):
            print(f"[{ps.index}]  {status[i]}  python3 {ps.name}.py \n")

    if "-l" in flags:
        print(f"[{ps.index}] {ps.Id} {status[i]}  python3 {ps.name}.py \n")

    elif "-p" in flags:
        print(f"Id {ps.Id}\n")



