# https://flask.palletsprojects.com/en/1.1.x/quickstart/
# pip3 install flask

import json

from flask import Flask
from flask import request, Response
from processor import process

app = Flask(__name__)


@app.route("/reverse")
def reverse():
    reply = process(app, request, reverse_data)
    return reply


def reverse_data(data: str) -> str:
    data = data + " " + data[::-1]
    return data


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4001)
