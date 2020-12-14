#!/usr/bin/env bash
# just a simple run script to start the servers and allow cleanup
# https://spin.atomicobject.com/2017/08/24/start-stop-bash-background-process/

trap "exit" INT TERM ERR
trap "kill 0" EXIT

# "processing steps" on 4000 and 4001
python3 processors/upper.py &
python3 processors/reverse.py &

# "coordinator" on 3001
python3 switchboard.py &

# "client" on 3000
python3 operator.py &

wait
