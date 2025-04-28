import signal
import os
from src.jobs import CHILD_BG
import psutil

def bg(cmd: str):
     """
     Resume the last paused process.
     """
     assert len(cmd) <= 2, "too many arguments"
     global CHILD_BG
     if len(CHILD_BG) == 0:
          print("No background process")
          return
     if len(cmd) == 1:
          child_ps = CHILD_BG[-1]
          proc = psutil.Process(child_ps.Id)
          os.kill(child_ps.Id, signal.SIGCONT)
     else:
          pid = cmd[1]
          try:
               pid = int(pid)
          except ValueError:
               raise ValueError("The pid should be an integer.")
          try:
               list_id = [child.Id for child in CHILD_BG]
               if pid not in list_id:
                    raise ValueError(f"The process with pid {pid} is not in the background")
               child_ps = CHILD_BG[list_id.index(pid)]
               CHILD_BG[list_id.index(pid)].status = 1
               os.kill(child_ps.Id, signal.SIGCONT)
          except ValueError:
               raise ValueError(f"The process {id} does not exist in the background.")
     print(f"The process {child_ps.name} resumes in the background.")