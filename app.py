#!/usr/bin/python3
# -*- coding: utf-8 -*-
from gensim.summarization import summarize
from bottle import route, run, response, Bottle, request
import json
from collections import OrderedDict
import re
import html2text
from selenium import webdriver
import time

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

    try:
        jsontext = request.json
    except:
        status = "false"
        response.content_type = 'application/json'
        message = "wrong json format"
        return json.dumps(OrderedDict(status=status, message=message))

    try:
        text = jsontext['text']
    except:
        status = "false"
        response.content_type = 'application/json'
        message = "have not text field"
        return json.dumps(OrderedDict(status=status, message=message))

    for i in [r'\\n', r'\\t', r'•']:
        text = re.sub(i, " ", text)
    text = re.sub(r'\s+', ' ', text)
    # print(text)

    urls = find_url(text)
    print (urls)
    privacy_url = get_privacy_url(urls)
    terms_url = get_terms_url(urls)
    try:
        description = summarize(text)
    except Exception as e:
        status = "false"
        message = str(e)
        return json.dumps(OrderedDict(status=status, message=message))
    response.content_type = 'application/json'
    privacy = ""
    if len(privacy_url) > 0:
        description = description + "\nPrivacy Policy: " + ", ".join(s for s in privacy_url)

        for i in privacy_url:
            privacy += summarize_from_link(i)

    terms = ""
    if len(terms_url) > 0:
        description = description + "\nTerms of Service: " + ", ".join(s for s in terms_url)
        for i in terms_url:
            terms += summarize_from_link(i)

    return json.dumps(OrderedDict(status=status, description=description, privacy=privacy, terms=terms))


@app.error(405)
def error405(error):
    response.content_type = 'application/json'
    status = "false"
    message = "405 Method not allowed"
    return json.dumps(OrderedDict(status=status, message=message))


def get_terms_url(urls):
    terms_urls = []
    for i in urls:
        if "terms" in i.lower():
            terms_urls.append(i)
    return terms_urls


def get_privacy_url(urls):
    privacy_urls = []
    for i in urls:
        if "privacy" in i.lower():
            privacy_urls.append(i)
    return privacy_urls


def find_url(text):
    return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)


def summarize_from_link(link):
    browser = webdriver.PhantomJS()
    browser.get(link)
    time.sleep(2)
    html = browser.page_source
    text = html2text.html2text(html)
    text = summarize(text)
    del browser
    if text is None:
        text=""
    return text


if __name__ == "__main__":
    run(app, host="0.0.0.0", port="9000", debug=False)
