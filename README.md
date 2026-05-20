#This is for the History Tracker Microservice

## 1. Desription

This is a microservice that tracks the history of visited URLs and returns a list of 
URLs back from most recently viewed to least. There are 4 different calls.

a. '/visit' which records the URL
b. '/setHome' which sets the home page and resets history
c. '/history' which will return the list of the current history
d. '/remove' which will remove the most recent url from the history list

Note: No duplicates will be on the list and a call to '/visit' while a URL is in the history list will move that url to the front of the list.

------------------------------------------------------------------------------------

## 2. How to run the microservice

```bash
python History_MS.py

Note: The service listens on 'Host: localhost' on 'Port: 8080' which has a base
URL of 'http://localhost:8080'

------------------------------------------------------------------------------------

## 3. Request 

To request data from this microservice, another program will need to send a HTTP GET request to one of the defined endpoints.

An example to record a visit: GET /visit?url=<page URL>
This would look like: http://localhost:8080/visit?url=club.html?id=1

A program can send this request by using Python's urllib library like this: 

import urllib.request
import urllib.parse

params = urllib.parse.urlencode({"url": "club.html?id=1"})
url = f"http://localhost:8080/visit?{params}"
urllib.request.urlopen(url)

------------------------------------------------------------------------------------

## 4. Recieve

After sending a request, the microservice will respond with JSON data.

An example is when calling /history, it will return: 
{"history": ["club.html?id=1", "club.html?id=2"]}

A program can recieve and parse through the JSON by using Python like: 

import urllib.request
import json

raw = urllib.request.urlopen("http://localhost:8080/history").read().decode()
data = json.loads(raw)

print(data["history"])
