import os
import time

def create_child_process():
    pid = os.fork()
    if pid == 0:
        # Child process
        print("Child process is running...")
        time.sleep(2)
        print("Child process is exiting...")
    else:
        # Parent process
        return pid

def main():
    child_pid = create_child_process()

    # Wait for the child process to terminate
    pid, status = os.waitpid(child_pid, 0)
    if pid == 0:
        print("No child process to wait for.")
    else:
        print(f"Child process {pid} terminated with status {status}.")

    # Try to wait for a non-existent child process
    pid, status = os.waitpid(-1, os.WNOHANG)
    if pid == 0:
        print("No child process to wait for.")
    else:
        print(f"Child process {pid} terminated with status {status}.")

if __name__ == "__main__":
    main()