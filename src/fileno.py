import io
list_file = ["bg.py", "fileno.py", "fg.py", "fileno.py", "run.py", "man.py"]
a, b, c, d, e, f = 0, 0, 0, 0, 0, 0
list_ref = [a, b, c, d, e, f]

for i, f in enumerate(list_file):
    list_ref[i] = open(f, 'r')
    list_ref[i].fileno() = 2
