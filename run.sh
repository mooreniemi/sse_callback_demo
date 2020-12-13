#!/usr/bin/env bash

# "processing steps" on 4000 and 4001
python3 processors/upper.py &
python3 processors/reverse.py &

# "coordinator" on 3001
python3 switchboard.py &

# "client" on 3000
python3 operator.py &
