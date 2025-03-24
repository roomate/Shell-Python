def echo(cmd: str):
    if len(cmd) <= 1:
        exit(0)
    else:
        txt = ''.join(cmd[1:])
        print(txt)