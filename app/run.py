#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import re
import time
from bottle import route, run, response, Bottle, request
from bs4 import BeautifulSoup
from collections import OrderedDict
from gensim.summarization import summarize
from selenium import webdriver



app = application = Bottle()

#
@app.error(404)
def error404(error):
    """error 404"""
    response.content_type = 'application/json'
    status = "false"
    message = "404 page not found, check api documentation"
    return json.dumps(OrderedDict(status=status, message=message))


@app.route('/')
def index():
    response.content_type = 'application/json'
    return "test"


@app.post('/api')
def api():
    status = "true"
    message = "None"
    response.content_type = 'application/json'

    """get json from post. validate"""
    try:
        jsontext = request.json
    except:
        status = "false"
        response.content_type = 'application/json'
        message = "wrong json format"
        return json.dumps(OrderedDict(status=status, message=message))

    """check text field"""
    try:
        text = jsontext['description']
    except:
        status = "false"
        response.content_type = 'application/json'
        message = "have not description field"
        return json.dumps(OrderedDict(status=status, message=message))

    """remove service symbol for summarize"""
    for i in [r'\\n', r'\\t', r'•']:
        text = re.sub(i, " ", text)
    text = re.sub(r'\s+', ' ', text)
    # print(text)

    """find urls"""
    urls = find_url(text)
    # print (urls)
    privacy_url = get_privacy_url(urls)
    terms_url = get_terms_url(urls)

    """summarize description"""
    try:
        description = summarize(text, ratio=0.1)
    except Exception as e:
        status = "false"
        message = str(e)
        return json.dumps(OrderedDict(status=status, message=message))

    """get and summarize privacy"""
    privacy = ""
    if len(privacy_url) > 0:

        for i in privacy_url:
            privacy += summarize_from_link(i)

    """get and summarize terms"""
    terms = ""
    if len(terms_url) > 0:

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
    """search terms url"""
    terms_urls = []
    for i in urls:
        if "terms" in i.lower():
            terms_urls.append(i)
    return terms_urls


def get_privacy_url(urls):
    """search privacy url"""
    privacy_urls = []
    for i in urls:
        if "privacy" in i.lower():
            privacy_urls.append(i)
    return privacy_urls


def find_url(text):
    """find http url"""
    return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)


def summarize_from_link(link):
    """phantomjs browser for content"""
    browser = webdriver.PhantomJS()
    browser.get(link)
    time.sleep(2)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    text_list = [string.text for string in soup.find_all('p')]
    text = ' '.join(text_list)
    text = summarize(text, ratio=0.02)
    del browser

    if text is None:
        text = ""
    return text


if __name__ == "__main__":
    run(app, host="0.0.0.0", port="9000", debug=False)
