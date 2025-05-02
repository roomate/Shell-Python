 # A Hell of a Shell

This project is my first experience dealing with the inner workings of an operating system, via Python programming language.

Here is my own Linux Shell, written in Python. At the most basic level, a shell is simply a command line interpreter to interact with the Operating System (OS). I assume from now on the reader possess the very minimum knowledge on what shell can do.

Implementing a shell with the unique capacity to run a program is quite straightforward, you simply need to code a parser for the command line, and then call the right command within the library **os** offered by [Python documentation](https://docs.python.org/3/library/os.html). For the command is not written in it, you can simply execute the very same binaries as the Linux shell, by calling it with the `os.execvp` command.

 Now, if you want to do something a little bit more involved, you might remember that, in a shell, the commands `CTRL+C` and `CTRL+Z` can respectively stop or pause a process. Implementing this kind of behavior is much less trivial, as it relies on low-level mechanisms of the GNU Linux OS. Another possibility is the piping of process. In my shell, I have implemented all of the above. You can see a list below of all the commands I have written (built-in to **my** shell), and explain what was my programming strategy for all the above.

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
| terminate | Terminate the shell, serialize history beforehand | |
| man | Display the manual related to a command | |
| ln | Create a hard or symbolink link | os.link & os.symlink |
| history | Display a browsable history of past commands | |
| jobs | Display all jobs | |
| run\_bg | Run the process in background  | |
| check\_bg | Check there is a '&' in the line command | |

The difference between built-in and non built-in methods is important because the shell program deals with them very differently. Therefore, you should be aware of their respective implementation.

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
To fork means replacing the calling process by a parent process and a child process. The child process is given its own **pid**, while the parent process inherits the same pid as the calling process. They are both run concurrently by the OS. However, when the children process has terminated, it is not directly suppressed by the OS. It first has to be reaped by the parent process beforehand, saying 'I did what I supposed to do, I can go in peace'. "terminated" here can have different meanings here, depending on the objective sought for, but the point here is that the child process have to let know in some way to the parent process that it can suppressed without issue by the OS. If by misfortune, the child process happens to be never reaped after terminating, it will turn into a [**zombie process**](https://en.wikipedia.org/wiki/Zombie_process), and might consumes resources and RAM memory for nothing. You do not want that, especially when your processor happens to deals with hundreds of concurrent processes.
In practice, the parent process is said to wait for the child process with the syscall [**os.waitpid**](https://docs.python.org/3/library/os.html#os.waitpid), meaning it temporarily pauses here until given the order to continue. Note that the parent and child process do necessarily have to belong to the same group of process. By default though, they actually do belong to the same group of process.

An obvious question now, why forking ? The answer lies once more in how non built-in methods are called by the process. The C program is ran by the syscall `execvp`. This command replaces the calling process with another one, and stops it once it executed the C file. Therefore, if you do not fork, you actually terminates your bash process after executing your command. It obviously contradicts the expected behaviour of a shell; that is, waiting for the user to enter a new command line after executing the previous one. When forking, this is the child process that is terminated after executing the file, and that is perfectly fine, you do not want it to do something else.

If you want a complete and visual display of the child+parent hierarchical relationship running on your computer, you can type [**pstree**](https://man7.org/linux/man-pages/man1/pstree.1.html) in your shell. 

## Signals
[Signals](https://docs.python.org/3/library/signal.html) are a way for processes to communicate preemptively, that is, with top level priority. For example, when you type CTRL+C on your keyboard while a foreground process is running, it is sent a signal that definitively stop it. You most often need to define signal handlers. They are functions called when a signal is sent by a process, allowing to treat, if necessary, each situation in its own manner. One can for example cite `SIGTSTP` or `SIGINT` for respectively interrupting or stopping a process. The signals are also central for multi-processing because they are heavily employed for `bg` and `fg` commands.

## In practice

A detail of implementation is that the bash process itself ignore the signals `SIGINT` and `SIGTSTP`. Thus, when forking, the child process inherits these handlers, but you want it to be actually sensible to them. You hence need to reactive it them by hand within the child process. 

As said above, the shell operates differently for built-in and non built-in commands. For built-in commands, you just need to import the related function within the script, and then call it. That's it. You see here how much command built-in can help prevent purposeless complicated mecanisms. 

For others, like briefly explained above, you first need to fork the calling process. Next, the child process is detached from the parent process group and is made leader of is own process group. That is realized with [`setpgid`](https://docs.python.org/3/library/os.html#os.setpgid) command. Like said above, you need to reactivate the signals `SIGINT` and `SIGTSTP`, because you actually want to be able to interrupt them if the user or the OS decided so. You have to connect it to controlling terminal, which serves as both the standard input and output. 
However, be careful, connecting a child process to the controlling terminal triggers both the signals `SIGTTIN` and `SIGTTOU` (one for the standard input, one for the standard output). It has the immediate effect to prematurely stop it, before it had the chance to execute your program. As solution is to deactivate these signals just before forking. The next step is to actually execute the C program with the API call `os.execvp`. 

Eventually, you need to reactivate the signals `SIGTTIN` and `SIGTTOU` once the child process has been reaped. The loop is definitely closed, the shell can go wait for another command!

Until now, I simply described what was supposed to happen if you put a single command (no fork) and without interrupting the child process by any mean. A complete shell should be able to easily treat this cases within the framework offered by `POSIX` standard.

### Handling background processes
If you pause the foreground process (by typing `man less; CTRL+Z` for example), or simply let it run in the background (via the letter `&`), then you want the parent process to continue, and wait for a new command line. Note that the child process still exists, but have its way in the background, whether running or paused. You can observe it via a `ps -aux` command for example, and read the `State` column. 
But remember; the parent process was originally supposed to stay still until the child process finishes for a precise reason, to reap by itself its children process. This "wait until you are paused or terminated" type of behaviour can fortunately be easily coded with the flags `WEXITED` and `WSTOPPED`, see [here](https://docs.python.org/3/library/os.html#os.WEXITED). 

Assume now that you enter `bg` command or `fg` in the command line interpreter. Since no parent process actually wait for it to finish anymore, it will not be reaped, and thus become a zombie process, and you do not want that. That's what the `child_handler` function in `signal_handler` module is for. By default deactivated, you need to use the signal [`SIGCHLD`](https://docs.python.org/3/library/signal.html#signal.SIGCHLD), that is triggered every time a child process is paused or terminated. You can see it in `main.py`

I made a global variable `CHILD_BG` that stores all the child process currently in the background. You can display them with the command `jobs`. Eventually, if you are interested in the state of a particular process with known `pid`, then you can use library [`psutil`](https://psutil.readthedocs.io/en/latest/).

## Piping
Another interesting feature of the shell is piping. Piping means connecting the input and output of a sequence of process following sequentially each other. To understand how piping work, you need to have a clear idea of what are **file descriptors**, and about the notion of **standard input/standard output** of a process. In the environment I work on, a process will have two choices to read external data: the standard input or the pipe. While it reads the standard input at first by default, you can actually change this behaviour and set the standard input as the pipe. Technically, a pipe is a temporary file (located on the RAM), and created with the syscall `pipe`, returning its set of file descriptors; one for writing and one for reading (respectively the input and output of the pipe). 

Consider a piped command of the form: `A|B|C`. The process associated with command `A` must have its standard input onnected to the terminal, and its standard output connected with the file descriptor associated to the pipe. The easiest way to do that is certainly using the `os.dup` command, which allows you to duplicate a file descriptor. For process associated to command `B`, its standard input and standard output are respectively connected to the output and input of the pipe. It is invisible to the controlling terminal. Eventually, the process associated to `C` will have only its standard input connected to the output of the pipe. This way, the pipe exactly played its role to stream i/o between piped commands.
