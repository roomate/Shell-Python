import os

import multiprocessing as mp
from multiprocessing import Process
p = Process(target=print, args=[1])
p.run()

p = Process(target=print, args=(1,))
p.run()