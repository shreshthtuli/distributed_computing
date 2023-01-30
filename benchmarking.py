import os
import time
import psutil
import subprocess
import numpy as np
import pandas as pd
from shutil import move
from joblib import Parallel, delayed

NUM_WORKERS = 2
NUM_CLIENTS = 2
NUM_TASKS_PER_CLIENT = 5

# Load results
fpath = './profiling/benchmarks.csv'
if os.path.exists(fpath):
	results = pd.read_csv(fpath, index_col=False)
else:
	results = pd.DataFrame({'Workers':[], 'Functions': [], 'Throughput': []})

def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

# Define client runs
def run_tasks():
	for _ in range(NUM_TASKS_PER_CLIENT):
		subprocess.run("python challenge.py", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		time.sleep(0.5)

for NUM_WORKERS in range(1, 5):
	for NUM_CLIENTS in range(1, 5):
		if np.where((results.Workers == NUM_WORKERS) 
			& (results.Functions == NUM_CLIENTS))[0].any():
			continue
		# NUM_WORKERS = 1; NUM_CLIENTS = 3
		# Start server
		p = subprocess.Popen(["python", "server.py", str(NUM_WORKERS)])
		time.sleep(5)

		from distribute_challenge import compute_this

		# Run benchmark
		ts = time.time()
		Parallel(n_jobs=NUM_CLIENTS)(delayed(run_tasks)() for _ in range(NUM_CLIENTS))
		te = time.time()
		throughput = NUM_CLIENTS * NUM_TASKS_PER_CLIENT / (te - ts)

		print("Throughput = ", throughput)

		# Save result
		new = [NUM_WORKERS, NUM_CLIENTS, throughput]
		results = results.append(pd.Series(new, index=results.columns[:len(new)]), ignore_index=True)
		results.to_csv(fpath, index=False)

		# Sleep
		kill(p.pid)
		time.sleep(5)
		move('./profiling/results_%d.csv' % NUM_WORKERS, './profiling/results_%d_%d.csv' % (NUM_WORKERS, NUM_CLIENTS))
		# exit()



