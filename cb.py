# https://flask.palletsprojects.com/en/1.1.x/quickstart/
# pip3 install flask
# export FLASK_APP=respond.py && flask run

import os
import socket

from flask import Flask
from flask import request
from markupsafe import escape
import requests
import time

from sseclient import SSEClient

import queue

from multiprocessing.connection import Listener
from multiprocessing import Process, Queue

app = Flask(__name__)


def echo(listen_to_addr, return_q):
    print("will listen to " + listen_to_addr)
    # listen for the emitted event
    # https://github.com/btubbs/sseclient/blob/master/sseclient.py
    messages = SSEClient(listen_to_addr)

    # blocks forever, listening
    # for msg in messages:
    #    print(msg)

    # just wait for one message then go, still blocks
    return_q.put(next(messages))


@app.route("/ssec")
def ssec():
    # pass over the args, get back listening address
    listen_to = requests.get("http://localhost:8080/q", params=request.args)

    response = "no_reply"
    if listen_to.status_code == 200:
        r_queue = Queue()
        p = Process(target=echo, args=(listen_to.text, r_queue,))
        p.start()

        # Wait for 50ms
        p.join(0.05)

        if p.is_alive():
            p.terminate()
            # p.kill()
            p.join()

        try:
            response = r_queue.get(block=False)
        except queue.Empty:
            pass

    return str(response)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
