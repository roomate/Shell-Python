import os

def tokenization(cmd: str):
    cmd = cmd.strip()
    cmd = cmd.split(";")
    noOfCommand = len(cmd) #Number of commands passed in the CLI
    return noOfCommand, cmd
    # out = []
    # for current_cmd in cmd:
    #     current_cmd = current_cmd.strip()
    #     out.append(current_cmd.split(" "))
    # return noOfCommand, out

if __name__ == '__main__':
    A = input()
    nb, res = tokenization(A)
    print(nb, res)
