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
	print("attempting http_post with data:\n{},\n headers: {}".format(data,headers))
	for e in data:
		print("{}: {}".format(e, data[e]))	
	req = ulib.Request(url, headers = headers)
	print(req)
	response = ulib.urlopen(req, json.dumps(data).encode("utf-8")).read().decode()
	print(response)
	response = json.loads(response)
	print(response)
	return response