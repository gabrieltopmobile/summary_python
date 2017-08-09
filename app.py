#!/usr/bin/python3
# -*- coding: utf-8 -*-
from gensim.summarization import summarize
from bottle import route, run, response, Bottle, request
import json
from collections import OrderedDict

app = Bottle()


@app.error(404)
def error404(error):
    response.content_type = 'application/json'
    status = "false"
    message = "404 page not found, check api documentation"
    return json.dumps(OrderedDict(status=status, message=message))


@app.route('/')
def index():
    response.content_type = 'application/json'
    data = []
    return "test"


@app.post('/api')
def api():
    status = "true"
    message = "Nothing"
    text = request.forms.get('text')
    print (text)
    try:
        message = summarize(text)
    except Exception as e:
        status = "false"
        message = str(e)

    return json.dumps(OrderedDict(status=status, message=message))


@app.error(405)
def error405(error):
    response.content_type = 'application/json'
    status = "false"
    message = "405 Method not allowed"
    return json.dumps(OrderedDict(status=status, message=message))


if __name__ == "__main__":
    run(app, host="0.0.0.0", port="9000", debug=False)
