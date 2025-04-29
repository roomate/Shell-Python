# A Hell of a Shell

This project is my first experience dealing with the inner workings with an operating system, via Python programming language.

Here is my own Linux Shell, written in Python. At the most basic level, a shell is simply a command line interpreter to interact with the Operating System (OS). If one considers only this functionality, then implementing a shell is quite straightforward, you simply need to code a parser for the command line, and then make the right syscall with the library **os** offered by [Python documentation](https://docs.python.org/3/library/os.html). Now, if you want to do something a little bit more involved, you can remember that, in a shell, the commands CTRL+C and CTRL+Z can respectively stop or pause a process. Implementing this kind of behavior is much less trivial, as it relies on low-level mechanisms of the Linux OS. Another possibility is the piping of process. In my shell, I have implemented all of the above. I shall make a list of all the command I have written, and explain what was my programming strategy for all the above.

| Script | Action | syscall |
| --- | --- | --- |
| cd | Change the current working directory | os.chdir | 
| ls | Display all the files in the current working directory | os.listdir|
| bg | Move jobs to the background | |
| fg | Move jobs to the foreground | |
| mkdir | Create a directory in the current working directory | os.mkdir |
| echo | echo the string to standard output | print |
| pwd shell | Print the working directory | os.getpwd | 
| rmdir | Remove a directory | os.rmdir |
| terminate | Terminate the shell | |
| man | Display the manual related to a command | |
| ln | Create a hard or symbolink link | os.link & os.symlink |
| history | Display a browsable history of the past commands | |
| jobs | Display all the jobs | |

In the Linux operating system, certain shell commands, such as **cd**, are said to be **built-in**. 
This means that they are built directly into the OS kernel, rather than into the software layers of the OS. Other commands are usually part of the POSIX standard and are written in C. You can find the corresponding binary on your own computer, in the /bin directory, assuming you are on a Linux system of course. The POSIX methods are executed differently by the shell than the built-in ones. The most obvious is that for the former, the shell actually fork the calling process into a child and parent process. Forking is a very common mechanism for an operating system, the parent and children processes are run concurrently, the parent waiting for the child process to "terminates". "terminates" can have different meanings here, depending on the objective sought for, but the important thing to keep in mind is that **the child process have to be reaped by the parent process to be cleanly suppressed by the OS**. If the child process happens to be never reaped after terminating, it will turn into a zombie process, and might consumes resources and RAM memory for nothing. To avoid that, it is key to handle correctly signal and multi-process mechanisms. I will take the time to describe the strategy I employed just below.

## Fork syscall
Fork a process means replacing the calling process by a parent process and a child process. As briefly mentioned above, there roles are not symetric in the sense that the child process has to be reaped by the parent process for it to be effectively terminated. They are run concurrently by the OS, so usually, the command entered by the user will be run by the child process, while the parent process simply waits for it to finish what it has to do before reaping it. This mechanism is very classical in multi-process framework. Also, it is very easy to implement with the syscall **os.waitpid**. When forking, the child process is given its own **pid**. If you want a complete and visual display of the child+parent hierarchical relationship running on your computer, you can type **pstree** in your shell. Note that the parent and child process do not need to belong to the same group of process, even if by default, they are. I'll go more in details afterwards, because to go further, one first need to introduce the notion of signals as an inter-process channel of communication.
## Signals
