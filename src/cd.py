import os
def chdir(cmd: str)-> None:
    assert len(cmd) <= 2, "Too many arguments"
    if len(cmd) == 1:
        os.chdir(os.environ["HOME"])
    try:
        os.chdir(os.path.abspath(os.path.join(os.getcwd(), cmd[1])))
    except FileNotFoundError:
        print(f"FileNotFoundError: No such file or directory: {os.path.join(os.getcwd(),cmd[1])}")