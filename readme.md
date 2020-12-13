# sse "callback" demo

This repo contains a very simple (non-Production) example of using
Server-Side Events (SSE) to decouple services. Message receipt is not
guaranteed in any way. Either the message is received within 50ms or you
receive `no_reply`.

### trying it

``` 
# to launch the 4 servers on 3000,3001,4000,4001 
./run.sh

# to test that they're communicating properly
./test.sh

# to try arbitrary sends
curl -s localhost:3000/ssec?m=howdy%20cowboy
```

### understanding it

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
