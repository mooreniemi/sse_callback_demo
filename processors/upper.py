# https://flask.palletsprojects.com/en/1.1.x/quickstart/
# pip3 install flask

import json

from flask import Flask
from flask import request, Response
from processor import process

app = Flask(__name__)


@app.route("/upper")
def upper():
    reply = process(app, request, upper_data, "http://localhost:4001/reverse")
    return reply


def upper_data(data: str) -> str:
    data = data + " " + data.upper()
    return data


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4000)
