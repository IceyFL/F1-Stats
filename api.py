#imports
import requests
import json



#get most recent session
def getRecentSessionID():
    sessionsURL = "https://api.openf1.org/v1/sessions"

    result = requests.get(sessionsURL) #send request
    
    #load request response as a json
    sessionsJSON = json.loads(result.content)

    #get recent session id from json
    sessionID = sessionsJSON[-1]["session_key"]

    return sessionID

#get drivers
def getDrivers():
    #get most recent session id
    sessionID = getRecentSessionID()

    #request drivers from that session
    driversURL = "https://api.openf1.org/v1/drivers?session_key=" + str(sessionID)

    result = requests.get(driversURL) #send request

    #load request response as a json
    DriversJSON = json.loads(result.content)

    return DriversJSON
