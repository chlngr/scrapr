## Create a flask app that returns a random number
## Single route



from flask import Flask, render_template, request, url_for
import requests, bs4, re, pprint, json


#create a flask app
app = Flask(__name__)

#if the flask app is in main, then run it, else do nothing
if __name__ == '__main__':
	app.run()



#define a route /, return some text with instructions
@app.route('/')
def homePage():
	return 'GO TO /random/ TO GET A RANDOM NUMBER. PASS A GEOCODED JSON TO /senator/ TO RETRIEVE YOUR SENATORS'

#define a route /random/, bind a function showRandom(), and return a random number
@app.route('/random/')
def showRandom():
	import random
	myRandom = random.random()
	return str(myRandom)

#define a route /senator that accepts the POST method only, access latitude and longitude and convert to floats, then pass to getMySenator
@app.route('/senator/', methods =['POST'])
def senatorPage():
		userLocation = request.get_json(force=True)
		userLatitude = float(userLocation['latitude'])
		userLongitude = float(userLocation['longitude'])
		yourSenators = json.dumps(getMySenator(userLatitude,userLongitude))
		return yourSenators


#python to get all the senators.  I suspect this should all live in a separate .py file but the file/folder structure in question is still obscure to me

def getAllSenators():

	#set a user agent header because the senate webpage requires it
	userHeaders = {
					'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
	}

	#define the url as a variable

	requestUrl = 'https://www.senate.gov/senators/contact'

	#get the webpage
	res = requests.get(requestUrl,headers=userHeaders)

	#use the commented out code if you want the program to continue
	#even if there is an error in the get request
	#otherwise, this will break on any html error
	#try:

	res.raise_for_status()

	#except Exception as exc:
	#	print('There was a problem %s' % (exc))

	#create the bs4 object, explicitly use the default parser to avoid a warning message

	workSoup = bs4.BeautifulSoup(res.text, "html.parser")

	#the content text class identifies the senators information, as well as some headers, including a list of the senators

	workList = workSoup.select('.contenttext')

	#however, the senator classes are in a special typoed class

	classList = workSoup.select('.contentext')

	#remove the header elements from the working data leaving only the senators' information
	#the length of the list should be 400 (4 x 100)
	#Name/Party/State, Address, Phone, Contact


	del workList[0:3]
	#Length should equal 400 when Senator Strange's contact information is uploaded

	#initialize an empty list
	senatorsList = []

	#create a list of four element dicts
	for i in range(0,99,1):

	#create intermediate variables for the parsed information, then use regex to correct
	#Luther Strange does not yet have a contact, handle using if statements to leave blank. Remove conditionality when his website us updated
	#Note - this handles middle initials well, but may not handle double-barreled last names correctly
			
			if i <= 84:
					workLastName = re.sub('\s|[()]','',workList[i*4].getText()).split('-')[0].split(',')[0]
					workFirstName = re.findall('[A-Z][a-z]*',re.sub('\s|[()]','',workList[i*4].getText()).split('-')[0].split(',')[1])[0]
					try:
							workMiddleName = re.findall('[A-Z][a-z]*',re.sub('\s|[()]','',workList[i*4].getText()).split('-')[0].split(',')[1])[1]
					except IndexError:
							workMiddleName = ''
					workParty = re.sub('\s|[()]','',workList[i*4].getText()).split('-')[1]
					workState = re.sub('\s|[()]','',workList[i*4].getText()).split('-')[2]
					workAddress = workList[i*4+1].getText()
					workPhone = workList[i*4+2].getText()
					workContact = workList[i*4+3].getText().split()[1]
					workClass = classList[i].getText()
			elif i == 85:
					workLastName = re.sub('\s|[()]','',workList[i*4].getText()).split('-')[0].split(',')[0]
					workFirstName = re.findall('[A-Z][a-z]*',re.sub('\s|[()]','',workList[i*4].getText()).split('-')[0].split(',')[1])[0]
					try:
							workMiddleName = re.findall('[A-Z][a-z]*',re.sub('\s|[()]','',workList[i*4].getText()).split('-')[0].split(',')[1])[1]
					except IndexError:
							workMiddleName = ''
					workParty = re.sub('\s|[()]','',workList[i*4].getText()).split('-')[1]
					workState = re.sub('\s|[()]','',workList[i*4].getText()).split('-')[2]
					workAddress = workList[i*4+1].getText()
					workPhone = workList[i*4+2].getText()
					workContact = ""
					workClass = classList[i].getText()
			else:
					workLastName = re.sub('\s|[()]','',workList[i*4-1].getText()).split('-')[0].split(',')[0]
					workFirstName = re.findall('[A-Z][a-z]*',re.sub('\s|[()]','',workList[i*4-1].getText()).split('-')[0].split(',')[1])[0]
					try:
							workMiddleName = re.findall('[A-Z][a-z]*',re.sub('\s|[()]','',workList[i*4].getText()).split('-')[0].split(',')[1])[1]
					except IndexError:
							workMiddleName = ''
					workParty = re.sub('\s|[()]','',workList[i*4-1].getText()).split('-')[1]
					workState = re.sub('\s|[()]','',workList[i*4-1].getText()).split('-')[2]
					workAddress = workList[i*4+1-1].getText()
					workPhone = workList[i*4+2-1].getText()
					workContact = workList[i*4+3-1].getText().split()[1]
					workClass = classList[i].getText()
			senatorDict = {'lastName': workLastName,'firstName': workFirstName,'middleName': workMiddleName,'partyAffiliation': workParty,'state': workState,'class': workClass,'officeAddress': workAddress,'contactFormURL': workContact,'contactTelephone': workPhone}
			senatorsList.append(senatorDict)

	#print the list of senators
	#pprint.pprint(senatorsList)
	return senatorsList

def reverseGeoRequest(latitude,longitude,APIKey):

# form the requests URL, specify JSON format for simplicity, handle non-200 responses with a generic error code

	requestURL = 'https://maps.googleapis.com/maps/api/geocode/json?latlng='+str(latitude)+','+str(longitude)+'&key='+APIKey

	response = requests.get(requestURL)

	if response.status_code != 200:
		returnValue = 'ERROR STATUS CODE: ' + str(response.status_code)

	else:
		returnValue = response.json()
		
	#print the response JSON
	#pprint.pprint(returnValue)
	return returnValue

## get a senator based on an input lat and long
def getMySenator(latitude,longitude):

#run the get all senators script
	senatorsList = getAllSenators()

#get command line input for lat and long
#FIXME build in error handling for invalid geolocations (non-numeric, out of range). move out of US validation up in code.


#set the API Key

	key = ''

#run the georequest
	location = reverseGeoRequest(latitude, longitude, key)['results'][0]['address_components']

#pull the state from the response json

	state = ''
	nonUS = True

	for i in range(0,len(location),1):
		#handle non-US countries
			if location[i]['types'][0] == 'country':
				if location[i]['short_name'] == 'US':
					nonUS = False
			if location[i]['types'][0] == 'administrative_area_level_1':
				state = location[i]['short_name']


	

	filteredList = [{'results': 'success','message': ''}]
	nonUSError = {'results': 'error','message': 'You input a non-US address.  Please rerun with a US geocode.'}


	for k in range(0,99,1):
		if senatorsList[k]['state'] == state:
			filteredList.append(senatorsList[k])
	

	if nonUS is False:
		pprint.pprint(filteredList)
		return filteredList

	else:
		return nonUSError


