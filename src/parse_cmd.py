import os

def parse_cmd(cmd: str):
    cmd = cmd.split(";")
    noOfCommand = len(cmd) #Number of commands passed in the CLI
    out = []
    for current_cmd in cmd:
        current_cmd = current_cmd.strip()
        out.append(current_cmd.split(" "))
    return noOfCommand, out

if __name__ == '__main__':
    A = input()
    nb, res = parse_cmd(A)
    print(nb, res)
