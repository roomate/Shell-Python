import os

def rmdir(cmd: str):
    assert len(cmd) > 1, "rmdir: missing operand"
    for file in cmd[1:]:
        assert os.path.exists(file), "FileNotFoundError: No such file or directory"
    for file in cmd[1:]:
        os.rmdir(file)
    exit(0)