#! /usr/bin/env python3
# Test the flask app.py

import requests, pprint, json

def getLatLong():
	status = False
	while status == False:
		print("Please enter your latitude in numbers only:")
		try:
			latitude = float(input())
			status = True
		except ValueError:
			status = False

	status = False
	while status == False:
		print("Please enter your longitude in numbers only:")
		try:
			longitude = float(input())
			status = True
		except ValueError:
			status = False

	userLocation = {'latitude': str(latitude),
			'longitude': str(longitude)}
	print(userLocation)

	status = False
	while status == False:
		print("Please enter the URL you would like to use. Make sure you use a valid URL")
		userURL = str(input())
		response = requests.post(userURL, json = userLocation)
		print(response.text)
		if response.status_code == 200:
			status = True
		else:
			status = False

getLatLong()