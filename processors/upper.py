# https://flask.palletsprojects.com/en/1.1.x/quickstart/
# pip3 install flask

import json

from flask import Flask
from flask import request, Response
import requests

app = Flask(__name__)


@app.route("/upper")
def upper():
    reply = "no_reply"
    if request.args.get("m") and request.args.get("listener_id"):
        # modify the m for the next processor
        reply = process(request.args.get("m"))
        args = request.args.copy()
        args["m"] = reply
        print("will pass upper output " + reply + " to reverse input")
        try:
            requests.get(
                "http://localhost:4001/reverse", params=args, timeout=0.0000000001,
            )
        except requests.exceptions.ReadTimeout:
            pass
    return reply


def process(data: str) -> str:
    data = data + " " + data.upper()
    return data


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4000)
