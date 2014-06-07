#! /usr/bin/env python

import os
import sys
import multiprocessing as mp
import subprocess
import time
import signal
from Queue import Empty
import numpy as np

#=============================================================================
def task(q):
    #--- loop until the q queue is empty
    while True:
        #--- pull a command of the cueue without blocking
        cmd, stay_alive = q.get()
        if not stay_alive:
            return

        #--- run the command under bash and wait for it to end
        p = subprocess.Popen(['bash', '-c', cmd])
        p.wait()

        #--- tell the queue that this task is done
        q.task_done()

#=============================================================================
def parallel(cmd_list, njobs=None, assume_hyperthread=True):
    #--- fill a joinable cueue with commands
    queue =  mp.JoinableQueue()

    #--- determine the number of cores
    n_cores = mp.cpu_count()
    if assume_hyperthread:
        if (n_cores % 2) == 0:
            n_cores = n_cores / 2

    #--- set the number of jobs to default if necesarry
    if njobs is None:
        njobs = n_cores

    #--- initialize an empty process list
    p_list = []


    #--- spin up njobs workers to tackle the queue
    for nn in range(njobs):
        p = mp.Process(target=task, args=(queue,))
        p.start()
        p_list.append(p)

    for cmd in cmd_list:
        queue.put((cmd, True))
    #--- wait until the queue is done
    queue.join()

    for p in p_list:
        queue.put(('', False))
    queue.join()


    #--- wait until all processes are done
    for p in p_list:
        p.join()

#=============================================================================
if __name__ == '__main__':

    #--- read the commands from stdin
    cmd_list = sys.stdin.readlines()

    #--- run commands in parallel
    parallel(cmd_list, njobs=10)
    #parallel(cmd_list, njobs=10, assume_hyperthread=True)

