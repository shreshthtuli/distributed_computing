import sys
import rpyc
import time
import subprocess
import threading
import pandas as pd
from copy import deepcopy
from rpyc.utils.server import ThreadedServer

SERVER_PORT = 18811
NUM_WORKERS = int(sys.argv[1])
WORKER_PORTS = range(SERVER_PORT + 1, SERVER_PORT + 1 + NUM_WORKERS)

busy = [0] * NUM_WORKERS
finished = 0

df = pd.DataFrame({'Timestamp':[], 'Busy': [], 'Finished': []})

lock = threading.Lock()

@rpyc.service
class ServerService(rpyc.Service):
    @rpyc.exposed
    def find_free_worker(self):
        global finished, busy, df
        if 0 not in busy: return -1
        index = busy.index(0)
        lock.acquire()
        busy[index] = 1
        new = [time.time(), deepcopy(busy), finished]
        df = df.append(pd.Series(new, index=df.columns[:len(new)]), ignore_index=True)
        lock.release()
        return WORKER_PORTS[index]

    @rpyc.exposed
    def free_worker(self, worker_port):
        global finished, busy, df
        lock.acquire()
        busy[WORKER_PORTS.index(worker_port)] = 0
        finished += 1
        new = [time.time(), deepcopy(busy), finished]
        df = df.append(pd.Series(new, index=df.columns[:len(new)]), ignore_index=True)
        df.to_csv('./profiling/results_%d.csv' % NUM_WORKERS)
        lock.release()

# Start workers
print('starting workers')
for worker_port in WORKER_PORTS:
    subprocess.Popen(["python", "worker.py", str(worker_port)])

# Start server
time.sleep(2)
print('starting server')
server = ThreadedServer(ServerService, port=SERVER_PORT)
server.start()