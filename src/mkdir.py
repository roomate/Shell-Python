import os
def mkdir(cmd: str):
    assert len(cmd) > 1, print("mkdir: missing operand.")

    for folder in cmd[1:]:
        os.mkdir(folder)
    exit(0)