# Distributed computing challenge

## Quick start

Install prerequisites:
```shell
pip install psutil numpy pandas==1.1.2 matplotlib rpyc
```

To run server:
```shell
python3 server.py <number of workers>
```
for instance for two workers: `python3 server.py 2`

To run a function (implemented in challenge.py), in each shell run:
```shell
python3 challenge.py
```

The environment states are saved in `./profiling/` folder. To visualize run
```shell
python3 grapher.py <csv file name>
```
for instance for two workers, the file created would be `results_2.csv`. This will output the overall throughput (completed tasks / time in seconds) and create two graphs in `./plots/` folder. `busy.pdf` shows the allocation for each worker with time. `throughput.pdf` shows the total throughput of the system with time. This also visualizes the result of benchmarking i.e. throughput in diverse cases (varying clients/functions from 1 to 4 and worker count 1 to 4, each profiling file already saved in the profiling folder).

## Details

We use the RPyC library to run remote procedure calls from clients. Each client asks for a free worker from the server and runs the function on that worker node. This pipeline works as follows:
1. The server (`server.py`) keeps the busy state of each worker in the `busy` list. It also runs an RPyC threaded service running two functions: one for providing the port of the first available worker (`find_free_worker()`) and the second to free the server when the job completes (`free_worker()`).
2. The client (`challenge.py`) calls the function `free_worker()` and gets a port of a free worker as soon one is available.
3. The client then calls the worker function `run_code()`, sending the definition of the function to be executed as an argument. 
4. The client receives the result from the worker and calls the function `free_worker()` to inform the server that the execution has completed.

As this is a threaded server, multiple clients can run functions asynchronously and in parallel.


## License

Apache-2.0-Clause. 
Copyright (c) 2023, Shreshth Tuli.
All rights reserved.

See License file for more details.
