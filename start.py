"""
CreateTime    : 2019/5/1 18:56
Author        : X
Filename      : start.py
"""

from flask import Flask, make_response

APP = Flask(__name__, static_folder='static', static_url_path='/apps')


@APP.route("/api/v1/automl/version", methods=["GET"])
def version():
    return make_response("v 1.0.0")


if __name__ == '__main__':
    APP.run(debug=True)