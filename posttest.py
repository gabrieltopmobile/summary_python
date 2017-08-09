#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
with open('testtext2',"r") as fin:
    text=fin.read()
print (text)
r = requests.post("http://10.4.12.35:9000/api", data={'text': text}, headers={"Content-Type": "application/text-plain; charset=UTF-8" })


