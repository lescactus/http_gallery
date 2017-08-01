#!/usr/bin/env python3
 
# export FLASK_APP=app.py
# export FLASK_DEBUG=1
# flask run

from flask import Flask
from flask import render_template
from flask import request
from flask import make_response


app = Flask(__name__)

# Main page
@app.route("/index/", methods=['GET'])
@app.route("/", methods=['GET'])
def main():
    return "Hello"





if __name__ == "__main__":
    app.run()