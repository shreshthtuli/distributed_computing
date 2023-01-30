# Distributed computing challenge

## Quick start

Install prerequisites:
```shell
pip install psutil numpy pandas matplotlib rpyc
```

To run server:
```shell
python3 server.py
```

To run a function (implemented in challenge.py), in each shell run:
```shell
python3 challenge.py
```

The environment states are saved in `./profiling/` folder. To visualize run
```shell
python3 grapher.py results_2.csv
```

## Details

We use the RPyC library to run remote procedure calls from clients. Each client asks for a free worker from the server and runs the function on that worker node. 


## License

Apache-2.0-Clause. 
Copyright (c) 2023, Shreshth Tuli.
All rights reserved.

See License file for more details.
