import subprocess
import sys
import os
import time

def run_local_task(cmd):
  p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                        shell=True, preexec_fn=os.setsid)
  out, err = p.communicate()
  print "Output"
  print out

def run_experiment():
  clients = [c for c in range(20, 200, 20)]
  for c in clients:
    cmd = './runscripts/smartrun.sh bftsmart.demo.microbenchmarks.ThroughputLatencyClient 1001 '+ str(c) +' 5000 4 2 false false'
    print cmd
    run_local_task(cmd)
    time.sleep(60)

run_experiment()
