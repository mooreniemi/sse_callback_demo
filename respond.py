# https://flask.palletsprojects.com/en/1.1.x/quickstart/
# pip3 install flask

import os
import json

from flask import Flask
from flask import request, Response
from markupsafe import escape

import time
from queue import Queue
from multiprocessing.connection import Client

app = Flask(__name__)

from collections import defaultdict
from uuid import uuid4

# not really using the Queue here
listeners = defaultdict(Queue)


@app.route("/q")
def add_to_q():
    # create a unique address to listen to
    listener_id = uuid4()
    if request.args.get("m"):
        # do whatever processing you'd do
        data = process(request.args.get("m"))
        # enque the processed data
        listeners[str(listener_id)].put(data)
    reply = "http://localhost:8080/ssep/" + str(listener_id)
    print("will call back " + reply)
    return reply


@app.route("/ssep/<listener_id>")
def ssep(listener_id):
    print("(currently there are " + str(len(listeners.keys())) + " listeners)")
    print("will read out the listeners for " + listener_id)
    # at this point we stop storing for this listener
    resp = listeners.pop(str(listener_id)).get()
    # format the sse specific stuff
    return Response(format_sse(resp), mimetype="text/event-stream")


def process(data: str) -> str:
    data = data + " " + data.upper()
    return data


def format_sse(data: str, event=None) -> str:
    msg = f"data: {data}\n\n"
    if event is not None:
        msg = f"event: {event}\n{msg}"
    return msg


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
