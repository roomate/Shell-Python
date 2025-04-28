import os
import sys

o_fd, i_fd = os.pipe()
pid = os.fork()
if pid == 0:
    print(sys.stdout.fileno())
    os.dup2(o_fd, 0)
    os.dup2(i_fd, 1)
    os.execvp('cat', ["cat"])
else:
    print(sys.stdout.fileno())
    os.dup2(i_fd, 1)
    print("rfefre")