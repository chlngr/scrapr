#! /usr/bin/env python3
# this establishes a function to take a latitude and longitude and makes an API call to google maps api
# returning a json
# documentation for google maps API at https://developers.google.com/maps/documentation/geocoding/start\
# google maps API key for my project on Alex's account = 'AIzaSyA5Q5fAjkKWE0eXJFuS9HediGcLW8C9dY0'
# request template for reverse geo code = https://maps.googleapis.com/maps/api/geocode/json?latlng=40.714224,-73.961452&key=YOUR_API_KEY

import requests, pprint

def reversegeorequest(latitude,longitude,APIKey):

# form the requests URL, specify JSON format for simplicity, handle non-200 responses with a generic error code

	requestURL = 'https://maps.googleapis.com/maps/api/geocode/json?latlng='+str(latitude)+','+str(longitude)+'&key='+APIKey

	response = requests.get(requestURL)

	if response.status_code != 200:
		returnValue = 'ERROR STATUS CODE: ' + str(response.status_code)

	else:
		returnValue = response.json()
		
	pprint.pprint(returnValue)
	return returnValue

reversegeorequest(40.714224,-73.961452,'AIzaSyA5Q5fAjkKWE0eXJFuS9HediGcLW8C9dY0')