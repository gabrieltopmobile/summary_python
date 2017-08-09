#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
with open('testtext2',"rb") as fin:
    text=fin.read()
r = requests.post("http://10.4.12.35:9000/api", data={'text': text})
print (json.loads(r.text)['message'])

