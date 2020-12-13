#!/usr/bin/env bash

EXPECTED="meow meow MEOW MEOW WOEM WOEM woem woem"

# just a basic test confirming the sse consumer retrieves processed string
RESPONSE=`curl -s localhost:3000/ssec?m=meow%20meow`

[ "$RESPONSE" != "$EXPECTED" ] && echo "replied: $RESPONSE"

[ "$RESPONSE" = "$EXPECTED" ] && echo [ "$RESPONSE" = "$EXPECTED" ]
