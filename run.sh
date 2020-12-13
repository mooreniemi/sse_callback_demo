#!/usr/bin/env bash

# "processing steps"
python3 upper.py &
python3 reverse.py &

# "coordinator"
python3 switchboard.py &

# "client"
python3 operator.py &
