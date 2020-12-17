```
        __
      /` _`\
     |  (_()| .-.
      \_  _/_/   \
        ||=[_]   |
        || | |   |
        ||/   \  |
        ||`---'  /
    .--'||-.___.'
  /`  .-||-.
  '-/`.____.`\
jgs '.______.'
```
[ascii art from here](https://www.asciiart.eu/electronics/phones)

# sse "callback" demo

This repo contains a very simple (non-Production) example of using
Server-Side Events (SSE) to decouple services. Message receipt is not
guaranteed in any way. Either the message is received within 50ms or you
receive `no_reply`.

A "client" server calls a "coordinator" server that forwards the request
to the first in a line of processors. The initial client server does not
wait for the http response of the processors, but instead gets
a `listener_id` like a ticket at the RMV and then waits for a SSE at that
address. After 50ms the client server "hangs up" and drops the message.

### trying it

After installing requirements, run `bin` scripts from root of project.

``` 
# to launch the 4 servers on 3000,3001,4000,4001 
./bin/run.sh

# to test that they're communicating properly
./bin/test.sh

# to try arbitrary sends
curl -s localhost:3000/ssec?m=howdy%20cowboy
```

### understanding it

#### project structure

```
├── bin
│   ├── run.sh # run the servers
│   └── test.sh # test everything works as expected
├── LICENSE
├── operator.py # the "client" that "calls" the first processor and waits
├── processors
│   ├── processor.py # shared code to hit next processor
│   ├── reverse.py # last processor
│   └── upper.py # first processor
├── readme.md
├── requirements.txt
└── switchboard.py # the "coordinator" that manages queue and sse

2 directories, 10 files
```

#### summary

The purpose of this setup is to make data flow in one direction. Each
processor needs to only know the address of the next processor (and obey
its API contract for input), or if they don't know it, the address of the
reply "sink" to finish the data flow.

```
The overall flow looks like this:

operator.py <-> switchboard.py -> upper.py -> reverse.py -> switchboard.py

We first hit the switchboard from the operator. The switchboard fires off
the request to the first processor and replies to the operator with the
SSE address to remain listening on.

operator.py <->> switchboard.py

The switchboard's request to the first processor includes the listener_id
so that the final processor, reverse, can label the data for return.

switchboard.py -> upper.py -> reverse.py -> switchboard.py

The switchboard has been polling its iternal listeners object on a timeout
and if it received a request to sink from reverse, now contains data it
can return to the operator via SSE, which has also been listening on
a timeout.

operator.py <<-> switchboard.py
```

