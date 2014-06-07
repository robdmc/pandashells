#! /usr/bin/env python

import os
import sys
import gevent
import subprocess
import time
import signal


from gevent.pool import Pool



def mop_up(x):
    print 'mopping up {}'.format(x)
    sys.stdout.flush()

def worker(x):
    print 'starting {}'.format(x)
    sys.stdout.flush()
    time.sleep(1)



pool = Pool(3)

#pool.apply_cb(worker, args=(1,),  callback=mop_up)
#pool.join()



#pool.map(worker, xrange(10), callback=mop_up)
pool.map_async(worker, xrange(10))
pool.join()
print 'done'
