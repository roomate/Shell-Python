import os
import sys

def ln(cmd):
    """
    Create a symbolic or hard link.
    """
    assert len(cmd) >= 1, "ln: missing file operand \n Try 'ln --help' for more information."

    if cmd[1] == '-s':
        assert cmd[3] not in os.listdir(), f"ln: failed to create symbolic link {os.path.join(cmd[2], cmd[1])}: File exists"
        assert cmd[2] in os.listdir(), f"ln: failed to access {cmd[2]}, No such file or directory"
        os.symlink(cmd[2], cmd[3])
        sys.exit(0)
    else:
        assert not os.isdir(os.path.normath(cmd[2])), f"ln: {cmd[2]}: hard link not allowed for directory"
        assert cmd[1] in os.listdir(), f"ln: failed to access {cmd[1]}, No such file or directory"
        os.link(cmd[1], cmd[2])
        sys.exit(0)