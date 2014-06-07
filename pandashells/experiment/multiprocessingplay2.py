#! /usr/bin/env python

import os
import sys
import multiprocessing
import subprocess
import time
import signal

##############################################################################
##This should work
#def init_worker():
#    signal.signal(signal.SIGINT, signal.SIG_IGN)
#
#def worker():
#    while(True):
#        time.sleep(1.1234)
#        print "Working..."
#
#if __name__ == "__main__":
#    pool = multiprocessing.Pool(50, init_worker)
#    try:
#        for i in range(50):
#            pool.apply_async(worker)
#
#        time.sleep(10)
#        pool.close()
#        pool.join()
#
#    except KeyboardInterrupt:
#        print "Caught KeyboardInterrupt, terminating workers"
#        pool.terminate()
#        pool.join()
#sys.exit()
##############################################################################

##############################################################################
#def mop_up(result):
#    print 'mopup'
#
#
#def worker(x):
#    signal.signal(signal.SIGINT, signal.SIG_IGN)
#    print 'starting', x
#    sys.stdout.flush()
#    time.sleep(10)
#    return x
#
#if __name__ == "__main__":
#    pool = multiprocessing.Pool(6)
#    try:
#        for i in range(100):
#            pool.apply_async(worker, args=(i,), callback=mop_up)
#
#        pool.close()
#        pool.join()
#
#    except KeyboardInterrupt:
#        print "\nCaught KeyboardInterrupt, terminating workers"
#        pool.terminate()
#        pool.join()
#        sys.exit(1)
#sys.exit()
##############################################################################



def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

#def worker():
#    while(True):
#        time.sleep(1.1234)
#        print "Working..."
def worker(x):
    print 'starting', x
    sys.stdout.flush()
    time.sleep(1 + x)
    return x

def mop_up(result):
    print 'finishing ', result
    sys.stdout.flush()


if __name__ == "__main__":
    pool = mp.Pool(3, init_worker)
    try:
        for i in range(5):
            #pool.apply_async(worker)
            pool.apply_async(worker, args = (i, ), callback=mop_up)

        pool.close()
        pool.join()

    except KeyboardInterrupt:
        print "Caught KeyboardInterrupt, terminating workers"
        sys.stdout.flush()
        pool.terminate()
        pool.join()


sys.exit()

def task(x):
    print 'starting', x
    sys.stdout.flush()
    time.sleep(10 + x)
    return x


pool = mp.Pool(3)

def handle_interrupt(signal, frame):
        print('Terminating all processes')
        pool.terminate()
        sys.exit(0)
signal.signal(signal.SIGINT, handle_interrupt)



def mop_up(result):
    print 'finishing ', result
    sys.stdout.flush()

if __name__ == '__main__':
    for i in range(1,5):
        pool.apply_async(task, args = (i, ), callback=mop_up)
    pool.close()
    pool.join()


