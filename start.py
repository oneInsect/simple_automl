"""
CreateTime    : 2019/5/1 18:56
Author        : X
Filename      : start.py
"""

from flask import Flask, make_response

APP = Flask(__name__, static_folder='static', static_url_path='/apps')


@APP.route("/", methods=["GET"])
def index():
    return make_response("Hello!")


if __name__ == '__main__':
    APP.run(debug=True)