#!/usr/bin/python3
# -*- coding: utf-8 -*-
from gensim.summarization import summarize
from bottle import route, run, response, Bottle, request
import json
from collections import OrderedDict
import re
import string

app = application = Bottle()


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
    message = "None"
    text = request.forms.text
    for i in [r'\\n', r'\\t', r'•']:
        text = re.sub(i, " ", text)
    text = re.sub(r'\s+', ' ', text)
    print(text)
    print(find_url(text))
    try:
        message = summarize(text)
    except Exception as e:
        status = "false"
        message = str(e)
    response.content_type = 'application/json'
    return json.dumps(OrderedDict(status=status, message=message))


@app.error(405)
def error405(error):
    response.content_type = 'application/json'
    status = "false"
    message = "405 Method not allowed"
    return json.dumps(OrderedDict(status=status, message=message))


def find_url(text):
    return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)


if __name__ == "__main__":
    run(app, host="0.0.0.0", port="9000", debug=False)
