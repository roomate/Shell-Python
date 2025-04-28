# A Hell of a Shell

Here is my own Linux Shell, written in Python. At the most basic level, a shell is simply a command line interpreter to interact with the Operating System (OS). If one considers only this functionality, then implementing a shell is quite straightforward, you simply need to code a parser for the command line, and then make the right syscall with the library **os** offered by [Python documentation](https://docs.python.org/3/library/os.html). Now, if you want to do something a little bit more involved, you can remember that, in a shell, the commands CTRL+C and CTRL+Z can respectively stop or pause a process. Implementing this kind of behavior is much less trivial, as it relies on low-level mechanisms of the Linux OS. Another possibility is the piping of process. In my shell, I have implemented all of the above. I shall make a list of all the command I have written, and explain what was my programming strategy for all the above.

| Script | Action | syscall |
| --- | --- | --- |
| cd | Change the current working directory | os.chdir | 
| ls | Display all the files in the current working directory | os.listdir|
| ---| ---| --- |
