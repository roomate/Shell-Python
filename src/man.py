PATH_MANUAL = r"/usr/share/man"
import glob
import gzip
import os

def man(cmd: str):
    filename = cmd[1]
    s = glob.glob(pathname= r"man[1-8]/" + filename + ".[1-8].gz", root_dir=PATH_MANUAL)
    if s == []:
        print(f"No manual entry for {filename}")
        exit(1)
    assert len(s) == 1, "There shouldn't be more than one manual."
    manual = s[0]
    with gzip.open(filename=os.path.join(PATH_MANUAL, manual), mode='rt', encoding = 'utf-8') as file:
        content = file.read()
    print(content)
    exit(0)