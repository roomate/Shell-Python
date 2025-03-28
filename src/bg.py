import signal
import os
from src.jobs import CHILD_PS

def bg(cmd: str):
     """
     Resume the last paused process.
     """
     assert len(cmd) > 2, "too many arguments"
     global CHILD_PS
     if len(cmd) == 1:
          child_ps = CHILD_PS[-1]
          os.kill(child_ps.Id, signal.SIGCONT)
     else:
          id = cmd[1]
          try:
               id = int(id)
          except ValueError:
               raise ValueError("The pid should be an integer.")
          try:
               list_id = [child.Id for child in CHILD_PS]
               child_id = list_id.index(id)
               os.kill(child_id, signal.SIGCONT)
          except ValueError:
               raise ValueError(f"The process {id} does not exist in the background.")
     print(f"The process {child_ps.name} resumes.")
     return