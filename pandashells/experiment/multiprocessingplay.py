#! /usr/bin/env python

import os
import sys
import multiprocessing
import subprocess
import time
import signal

###############################################################################
###new version to try
#def worker(i):
#    try:
#        #print '+: %d %d' % (os.getpid(), i)
#        print '+: %d' % ( i)
#        sys.stdout.flush()
#        time.sleep(2)
#        return 'Success'
#    except KeyboardInterrupt, e:
#        #print '     -: %d %d' % (os.getpid(), i)
#        print '    -: %d' % ( i)
#        sys.stdout.flush()
#        pass
#
#pool = multiprocessing.Pool(10)
#p = pool.map_async(worker, range(160))
#try:
#    results = p.get(0xFFFF)
#except KeyboardInterrupt:
#    print 'parent received control-c'
#    sys.stdout.flush()
#    sys.exit(0)
#
#for i in results:
#    print i
#
#sys.exit()
#
###############################################################################

##############################################################################

#=============================================================================
def worker(cmd):
    #--- ignoring keyboard interupts allows for killing all childeren
    #    by killing parent.  Not sure why.
    try:
        p = subprocess.Popen(['bash','-c', cmd])
        p.wait()
        #sys.stdout.flush()
        #time.sleep(200)
    except KeyboardInterrupt, e:
        pass

if __name__ == '__main__':

    #--- define some fake commands
    cmd_list = ["echo c{}; sleep 200; echo done" .format(nn) 
            for nn in range(200)]

    #--- create a worker pool
    pool = multiprocessing.Pool(10)

    #--- assyncronously process the commands
    p = pool.map_async(worker, cmd_list)

    #--- this is a weird hack that allowws killing all children with ctrl-c
    try:
        results = p.get(0xFFFF)
    except KeyboardInterrupt:
        print '\nkilling all subprocesses'
        sys.stdout.flush()
        sys.exit(0)


    sys.exit()

##############################################################################




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

#############################################################################
def mop_up(result):
    print 'mopup'


def worker(x):
    try:
        print 'starting', x
        sys.stdout.flush()
        time.sleep(10)
        return x
    except KeyboardInterrupt:
        print 'killing',x
        return None

if __name__ == "__main__":
    pool = multiprocessing.Pool(6)
    try:
        for i in range(100):
            pool.apply_async(worker, args=(i,), callback=mop_up)

        pool.close()
        pool.join()

    except KeyboardInterrupt:
        print "\nCaught KeyboardInterrupt, terminating workers"
        pool.terminate()
        pool.join()
        sys.exit(1)
sys.exit()
#############################################################################



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


