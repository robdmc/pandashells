#! /usr/bin/env python

import os
import sys
import multiprocessing as mp
import subprocess
import time
import signal
from Queue import Empty
import numpy as np
import csv
import datetime
import json

F_LIST = [
            '__job__activity',
            'job_num',
            'job_tot',
            'duration_sec',
            'duration_min',
            'duration_hr',
            'pid',
            'time_stamp',
            'cmd'
         ]

queue =  mp.JoinableQueue()
q = queue

#=============================================================================
def _task(verbose=False, suppress_cmd=True, suppress_stdout=False,
        suppress_stderr=False):

    #--- set destination of stderr and stdout
    stdout = subprocess.PIPE if suppress_stdout else None
    stderr = subprocess.PIPE if suppress_stdout else None

    #--- loop until the q queue is empty
    while True:
        try:
            #--- pull a command of the cueue without blocking
            job_num, job_tot, cmd = q.get(block=False)

            print os.getpid(), 'running',job_num
            sys.stdout.flush()

            if verbose:
                #--- define a record for logging
                rec = {
                        '__job__activity': '__job__start',
                        'job_num': job_num,
                        'job_tot': job_tot,
                        'time_stamp':str(datetime.datetime.now()),
                        'duration_sec': '',
                        'duration_min': '',
                        'duration_hr': '',
                        'pid': os.getpid(),
                        'cmd':cmd.strip(),
                        }
                #--- suppress command if requested
                if suppress_cmd:
                    rec['cmd'] = ''
                writer = csv.DictWriter(sys.stdout, F_LIST, extrasaction='ignore')
                writer.writerow(rec)
                sys.stdout.flush()

            #--- run the command under bash and wait for it to end
            #p = subprocess.Popen(['bash', '-c', cmd])
            p = subprocess.Popen(['bash', '-c', cmd], stdout=stdout,
                    stderr=stderr)
            p.wait()

            #--- tell the queue that this task is done
            q.task_done()
        #--- if the cueue was empty, get out of here
        except Empty:
            print 'ending',os.getpid()
            break

#=============================================================================
def parallel(cmd_list, njobs=None, verbosity=0, assume_hyperthread=True):
    #--- fill a joinable cueue with commands
    #queue =  mp.JoinableQueue()
    for ind, cmd in enumerate(cmd_list):
        job_num, job_tot = ind + 1, len(cmd_list)
        queue.put((job_num, job_tot, cmd))

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


    #--- 
    suppress_cmd = True
    suppress_stdout = True
    suppress_stderr = True
    verbose = False

    if suppress_cmd:
        F_LIST.pop(-1)

    if verbose:
        #--- write csv header
        writer = csv.DictWriter(sys.stdout, F_LIST)
        writer.writeheader()
        sys.stdout.flush()

    #--- spin up njobs workers to tackle the queue
    for nn in range(njobs):
        p = mp.Process(target=_task, args=(verbose, suppress_cmd,
            suppress_stdout, suppress_stderr))
        p.start()
        p_list.append(p)

    #--- wait until the queue is done
    queue.join()

    #--- wait until all processes are done
    for p in p_list:
        p.join()

#=============================================================================
if __name__ == '__main__':
    cmd_list = sys.stdin.readlines()
    parallel(cmd_list, njobs=10)

