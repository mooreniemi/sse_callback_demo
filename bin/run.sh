#!/usr/bin/env bash
# just a simple run script to start the servers and allow cleanup
# https://spin.atomicobject.com/2017/08/24/start-stop-bash-background-process/

# where the ports live
. ./bin/.env

trap "exit" INT TERM ERR
trap "kill 0" EXIT

########################################################
#  you can see dependencies below given port mappings  #
########################################################

# "processing steps" all might be final exit so they know switchboard
SWITCHBOARD_PORT=$SWITCHBOARD_PORT REVERSE_PORT=$REVERSE_PORT python3 processors/reverse.py &
SWITCHBOARD_PORT=$SWITCHBOARD_PORT REVERSE_PORT=$REVERSE_PORT UPPER_PORT=$UPPER_PORT python3 processors/upper.py &

# "coordinator" knows where it first calls (upper) and switchboard
SWITCHBOARD_PORT=$SWITCHBOARD_PORT UPPER_PORT=$UPPER_PORT python3 switchboard.py &

# "client"
SWITCHBOARD_PORT=$SWITCHBOARD_PORT OPERATOR_PORT=$OPERATOR_PORT python3 operator.py &

wait
