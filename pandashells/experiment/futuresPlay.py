#! /usr/bin/env python
import string
import futures
import time
import subprocess


cmd_list = ['echo 1_{:0d}; sleep 3; echo 2_{:0d}; sleep 3'.format(nn,nn) for nn in xrange(10)]
cmd_list = ['touch 1_{:0d}'.format(nn) for nn in xrange(10)]
#print cmd_list

def run_cmd(cmd):
    #print '---', cmd
    p = subprocess.Popen(['bash','-c',cmd] )
    print p
    #p = subprocess.Popen(['bash','-c',cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #sys.stdout.write(p.stdout.read())
    #sys.stderr.write(p.stderr.read())
    p.wait()
    print p.status
    sys.stdout.flush()
    #time.sleep(3)
    #os.system(cmd)
with futures.ProcessPoolExecutor(10) as pool:
    job_dict = {pool.submit(run_cmd, cmd):cmd for cmd in cmd_list}
    for job in futures.as_completed(job_dict):
        pass
        #print 'done'  #, job_dict[job]
