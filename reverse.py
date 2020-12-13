# https://flask.palletsprojects.com/en/1.1.x/quickstart/
# pip3 install flask

import json

from flask import Flask
from flask import request, Response
import requests

app = Flask(__name__)


@app.route("/reverse")
def reverse():
    reply = "no_reply"
    if request.args.get("m") and request.args.get("listener_id"):
        listener_id = request.args.get("listener_id")
        reply = process(request.args.get("m"))
        args = request.args.copy()
        args["m"] = reply
        # last processor in the chain, so reply to sink
        print("will pass reverse output " + reply + " to sink")
        try:
            requests.get(
                "http://localhost:3001/sink_to/" + listener_id,
                params=args,
                timeout=0.0000000001,
            )
        except requests.exceptions.ReadTimeout:
            pass
    return reply


def process(data: str) -> str:
    data = data + " " + data[::-1]
    return data


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4001)
