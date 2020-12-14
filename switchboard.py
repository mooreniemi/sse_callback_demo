# https://flask.palletsprojects.com/en/1.1.x/quickstart/
# pip3 install flask

import os
import json

from flask import Flask
from flask import request, Response
from markupsafe import escape

import time
import requests
from queue import Queue
from multiprocessing.connection import Client

app = Flask(__name__)

from collections import defaultdict
from uuid import uuid4

# not really using the Queue here
listeners = defaultdict(Queue)


@app.route("/flush")
def flush():
    # just in case you want to clear the listeners manually
    listeners = defaultdict(Queue)
    return 'ok'


@app.route("/sink_to/<listener_id>")
def sink(listener_id):
    app.logger.debug("sinking data to " + listener_id)
    if request.args.get("m"):
        data = request.args.get("m")
        # enque the processed data in this server's memory
        listeners[str(listener_id)].put(data)
    else:
        app.logger.error("did you mean to do an empty sink?")
    return listener_id


@app.route("/q")
def add_to_q():
    # create a unique address to listen to
    listener_id = str(uuid4())

    # forward the m argument on to the first processor
    if request.args.get("m"):
        args = request.args.copy()
        args["listener_id"] = listener_id
        try:
            requests.get(
                "http://localhost:4000/upper", params=args, timeout=0.0000000001,
            )
        except requests.exceptions.ReadTimeout:
            pass

    # inform the caller of where to listen to the response
    reply = "http://localhost:3001/ssep/" + listener_id
    app.logger.debug("will call back " + reply)
    return reply


@app.route("/ssep/<listener_id>")
def ssep(listener_id):
    t_end = time.time() + 0.049
    resp = "timed_out"
    while time.time() < t_end:
        listeners_count = len(listeners.keys())

        if listeners_count:
            app.logger.debug("(currently there are " + str(listeners_count) + " listeners)")
            app.logger.debug("will read out the listeners for " + listener_id)
            try:
                resp = listeners.pop(listener_id).get()
                break
            except KeyError:
                pass

    # format the sse specific stuff
    return Response(format_sse(resp), mimetype="text/event-stream")


def format_sse(data: str, event=None) -> str:
    msg = f"data: {data}\n\n"
    if event is not None:
        msg = f"event: {event}\n{msg}"
    return msg


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3001)
