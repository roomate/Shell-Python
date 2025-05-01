 # A Hell of a Shell

This project is my first experience dealing with the inner workings of an operating system, via Python programming language.

Here is my own Linux Shell, written in Python. At the most basic level, a shell is simply a command line interpreter to interact with the Operating System (OS). If one considers only this functionality, then implementing a shell is quite straightforward, you simply need to code a parser for the command line, and then make call the right command within the library **os** offered by [Python documentation](https://docs.python.org/3/library/os.html). For complicated commands, you simply execute the very same binaries as the shell, with `os.execvp` command. Now, if you want to do something a little bit more involved, you might remember that, in a shell, the commands `CTRL+C` and `CTRL+Z` can respectively stop or pause a process. Implementing this kind of behavior is much less trivial, as it relies on low-level mechanisms of the GNU Linux OS. Another possibility is the piping of process. In my shell, I have implemented all of the above. You can see a list below of all the commands I have written (built-in to **my** shell), and explain what was my programming strategy for all the above.

| Script | Action | Python os command |
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
| history | Display a browsable history of past commands | |
| jobs | Display all jobs | |
| run\_bg | Run the process in background  | |
| check\_bg | Check there is a '&' in the line command | |

The difference between built-in and non built-in methods is important because the shell program deals with them very differently. Therefore, you should be aware of some differences.

### Built-in commands
In the GNU Linux operating system, certain shell commands, such as `cd` and `exit`, are said to be shell **built-in**. A list is available [here for GNU implementation](https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html). It basically means that they are directly incorporated into the shell program by itself; no external application intervenes, all the necessary resources are already at hands within the shell. Note also the existence of **bash** built-in commands, also frequently used in the shell, such as `echo`. Some commands can not be implemented via an external program, because they need direct access to the state of the shell process itself.

### Non built-in commands 
      
In contrast, non built-in commands do not exist within the shell application itself, they belongs to some external software. 
The very majority of them are located in the GNU **coreutils** or the **C Standard library**, written in C or Bash language. Hence, they belong to higher-level software layers of the OS . The corresponding executables are on your own computer, in the `/bin` directory (for Linux OS). When you call such a programm, the shell will fetch it via the `$PATH` environment variable. Common examples are `ls`, `ln` or `mkdir`. 
Also, the shell actually `fork` the calling process into a **child** and **parent** process, meaning the binary is executed in its own environment, different to that of the shell. 

Please, keep in mind that both built-in and non built-in, for the most part of them, abide by the [POSIX](https://fr.wikipedia.org/wiki/POSIX) standard. 

But what is a fork ? 

## `Fork` syscall
This syscall is a very common, yet costly, mechanism for an operating system when multi-processing comes into play, and becomes necessary.
To fork means replacing the calling process by a parent process and a child process. The child process is given its own **pid**, while the parent process inherits the same pid as the calling process. They are both run concurrently by the OS. However, when the children process has terminated, it is not directly suppressed by the OS. It has to be reaped by the parent process beforehand. "terminated" here can have different meanings here, depending on the objective sought for, but the point here is that the child process have to let know in some way that the parent process that it can suppressed without issue by the OS. If by misfortune, the child process happens to be never reaped after terminating, it will turn into a [**zombie process**](https://en.wikipedia.org/wiki/Zombie_process), and might consumes resources and RAM memory for nothing.
In practice, the parent process is said to wait for the child process with the syscall [**os.waitpid**](https://docs.python.org/3/library/os.html#os.waitpid), meaning it temporarily pauses here until given the order to continue. Note that the parent and child process do not need to belong to the same group of process, even if by default, they are. 

If you want a complete and visual display of the child+parent hierarchical relationship running on your computer, you can type [**pstree**](https://man7.org/linux/man-pages/man1/pstree.1.html) in your shell. 

## Signals
[Signals](https://docs.python.org/3/library/signal.html) are a way for processes to communicate preemptively, that is, with top level priority. For example, when you type CTRL+Z on your keyboard while a foreground process is running, it is sent a signal that definitively stop it. You most often need to define signal handlers. They are functions called when a signal is sent by a process, allowing to treat, if necessary, each situation in its own manner. One can for example cite `SIGTSTP` or `SIGINT` for respectively interrupting or stopping a process. The signals are also central for multi-processing because they are heavily employed for the `bg` and `fg` commands.

A group of process is a bunch of processed gathered together under same process group `pgid`, usually coinciding with the leader's `pid`.

## In practice

A detail of implementation is that the bash process itself ignore the signals `SIGINT` and `SIGTSTP`. Thus, when forking, the child process inherits the signal handlers. 

As said above, the shell operates differently for built-in and non built-in commands. For built-in commands, you just need to import the function within the script, and then call it. 

For others, like briefly explained above, you first need to fork the calling process. Then, the child process is detached from the parent process group and made leader of is own process group. That is realized with [`os.setpgid`](https://docs.python.org/3/library/os.html#os.setpgid). In the child process, you thus need to reactivate these signals, because you actually want to be able to interrupt them if necessary. Also, you have to connect it to controlling terminal, which serves as both the standard input and output. 
However, be careful, connecting a child process to the controlling terminal triggers both the signals `SIGTTIN` and `SIGTTOU`, which has the effect to stop it. You have to deactivate them beforehand. You can then execute the C script with `os.execvp`, and that's it! Or not exactly. You still need to reactivate the signals `SIGTTIN` and `SIGTTOU`.

### An important practical detail
If you pause the foreground process (via `man less; CTRL+Z` for example), then you want the parent process to continue, so that it can wait for the user to enter a new command line. Remember; it was supposed to stay still until the child process finishes, to reap it afterwards. This "wait until you are paused or terminated" behaviour can fortunately be codedwith the flags `WEXITED` and `WSTOPPED`, available [here](https://docs.python.org/3/library/os.html#os.WEXITED). 

Assume now that you enter `bg` command or `fg` in the command line interpreter. Since no parent process actually wait for it to finish anymore, it will not be reaped, and thus become a zombie process, and you do not want that. That's what the `child_handler` function in `signal_handler` module is for. By default deactivated, you need to use the signal [`SIGCHLD`](https://docs.python.org/3/library/signal.html#signal.SIGCHLD), that is triggered every time a child process is paused or terminated. You can see it in `main.py`

## Piping
Another interesting feature of the shell is piping. Piping means connecting the input and output of a sequence of process following each other. To understand how piping work, you need to have a clear idea of what are file descriptors, and the notion of standard input/ standard output of a process.
