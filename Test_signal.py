import time
import signal

def interrupt_handler(signum, frame):
	print("You are trying to interrupt me")

signal.signal(signal.SIGINT, interrupt_handler)

while 1:
	time.sleep(5)
	print("Hey")
