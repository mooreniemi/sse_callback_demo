#!/usr/bin/env bash

# just a basic test confirming the sse consumer retrieves processed string
RESPONSE=`curl -s localhost:3000/ssec?m=meow%20meow`
[ "$RESPONSE" = "meow meow MEOW MEOW" ] && echo [ $RESPONSE = "meow meow MEOW MEOW" ]
