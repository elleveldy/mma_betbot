import urllib.request as ulib
import uuid
import json


def http_get(url, headers):
	req = ulib.Request(url, headers=headers)
	print(str(req))
	responseData = ulib.urlopen(req).read()
	balance = json.loads(responseData.decode('utf-8'))
	return balance

def http_post(url, data, headers):
	req = ulib.Request(url, headers = headers)
	response = ulib.urlopen(req, json.dumps(data).encode("utf-8")).read().decode()
	response = json.loads(response)
	print(response)
	return response