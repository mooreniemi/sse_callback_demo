# https://flask.palletsprojects.com/en/1.1.x/quickstart/
# pip3 install flask
# export FLASK_APP=respond.py && flask run

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

@app.route('/q')
def add_to_q():
    listener_id = uuid4()
    if request.args.get('m'):
        msg_event = format_sse(request.args.get('m'))
        listeners[str(listener_id)].put(msg_event)
    reply = 'http://localhost:8080/ssep/' + str(listener_id)
    print('will call back ' + reply)
    return reply

@app.route('/ssep/<listener_id>')
def ssep(listener_id):
    print(list(listeners.keys()))
    print('will read out the listeners for ' + listener_id)
    # at this point we stop storing for this listener
    resp = listeners.pop(str(listener_id)).get()
    return Response(resp, mimetype='text/event-stream')

@app.route('/respond', methods=['POST'])
def respond():
    print(f"will callback {request.json['host']}:{request.json['port']}")
    hn = os.getenv('HOSTNAME')
    if not hn:
        hn = "local"
    q = "meow"
    if request.args.get('q'):
        q = request.args.get('q')

    time.sleep(0.001)
    host = request.json['host']
    port = request.json['port']
    conn = Client((host,port), authkey=b'secret password')
    conn.send({'q': q, 'hn': hn})
    conn.send({'more': 'data', 'one': 2})
    conn.send('close')
    conn.close()

    return 'ok'

def format_sse(data: str, event=None) -> str:
    msg = f'data: {data}\n\n'
    if event is not None:
        msg = f'event: {event}\n{msg}'
    return msg

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
