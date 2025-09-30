#imports
import requests
import json

#base link
global APILINK
APILINK = "https://api.openf1.org/v1/"


#basic functions

#get race sessions
def getSessionIDs(year=None, session_type = "Race"):
    
    if year != None: #add year parameter if mentioned
        sessionsURL = APILINK + f"sessions?session_type={session_type}&year={str(year)}"
    else:
        sessionsURL = APILINK + f"sessions?session_type={session_type}"

    result = requests.get(sessionsURL) #send request
    
    #load request response as a json
    sessionsJSON = json.loads(result.content)

    sessionIDs = [] #initialize list

    for session in sessionsJSON: #iterate through sessions
        sessionIDs.append(session["session_key"]) #add session ID to list

    return sessionIDs

#get most recent session
def getRecentSessionID():
    sessionsURL = APILINK + "sessions"

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
    driversURL = APILINK + "drivers?session_key=" + str(sessionID)

    result = requests.get(driversURL) #send request

    #load request response as a json
    DriversJSON = json.loads(result.content)

    return DriversJSON



#more functions

#get average points this year for a driver
def getSeasonInfo(driver_number):

    #get all race ids from this season
    raceSessions = getSessionIDs(year=2025)

    #initialize variables
    racesEntered = 0
    totalPoints = 0

    #get all race results
    raceResults = requests.get(APILINK + f"session_result?driver_number={str(driver_number)}")

    #load as json
    racesJSON = json.loads(raceResults.content)

    for race in racesJSON: #iterate over each race
        if race["session_key"] in raceSessions: #if this race is in the raceID list
            totalPoints += race["points"] #add points to total
            racesEntered += 1 #add 1 to races entered

    #avoid division by 0
    if racesEntered == 0: return [0,0]

    #calculate average
    averagePoints = totalPoints / racesEntered

    return [averagePoints, racesEntered]