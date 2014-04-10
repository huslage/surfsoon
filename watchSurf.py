#!env python

import json
import requests
from sseclient import SSEClient
import datetime
import pytz

def toStars(rating):
	b = ""
	for i in range(0,rating):
		b += "*"
	return b  

accessToken = '1684e29738b4770c1623fee36778c291a1b55eab'
sparkID = '48ff6c065067555010342387'


msApiKey = 'jPZN3le3Rj1L3OXqwr9sjgYZUJ86imkm'
msBaseUrl = "http://magicseaweed.com/api/" + msApiKey + "/forecast/?spot_id=";
msParams = { "units": "us", "fields": "timestamp,swell.*,wind.speed,wind.unit,solidRating" }

posturl = 'https://api.spark.io/v1/devices/'+sparkID+'/surf'
postheaders = {'Content-Type': 'application/x-www-form-urlencoded'}
postparams = {}
postparams['access_token'] = accessToken

spots = {
"2456": "Playa Guiones",
"362": "Higgins Beach",
"852": "Old Orchard Beach",
"401": "Topsail Island",
"650": "Carolina Beach",
}

h = {"Authorization" : "Bearer " + accessToken}
r = SSEClient('https://api.spark.io/v1/events/refresh', headers=h)

for l in r:
	try:
		j = json.loads(l.data)
		spotID = j['data']

		if spotID == "0":
			postparams['args'] = "/Up next,/Surf report!"
			ps = requests.post(posturl,data=postparams,headers=postheaders)
		else:
			msUrl = msBaseUrl + spotID
			cb = requests.get(msUrl, params=msParams)
			ms =  cb.json()

		#spotName = spots[spotID]
		spotName = spotID


		time = datetime.datetime.now(pytz.timezone("America/New_York")).strftime("%m-%d-%Y at %R:%M")

		today = ms[4]
		tomorrow = ms[12]
		todayrating = toStars(today["solidRating"])
		tomorrowrating = toStars(tomorrow["solidRating"])

		todaystr = "Today {}-{}ft {} {}{}".format(today["swell"]["minBreakingHeight"],today["swell"]["maxBreakingHeight"],todayrating,today["wind"]["speed"],today["wind"]["unit"])
		tomorrowstr = "Manana {}-{}ft {} {}{}".format(tomorrow["swell"]["minBreakingHeight"],tomorrow["swell"]["maxBreakingHeight"],tomorrowrating,tomorrow["wind"]["speed"],tomorrow["wind"]["unit"])
		
		updatestr =  "{}/{}/{}/{}".format(spotName,todaystr,tomorrowstr,time)
		postparams['args'] = updatestr

		ps = requests.post(posturl,data=postparams,headers=postheaders)

	except ValueError:
		pass
