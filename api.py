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
        sessionsURL = APILINK + f"sessions?session_name={session_type}&year={str(year)}"
    else:
        sessionsURL = APILINK + f"sessions?session_name={session_type}"

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

    #get all race and qualy ids from this season
    raceSessions = getSessionIDs(year=2025)
    qualySessions = getSessionIDs(year=2025,session_type="Qualifying")

    #initialize variables
    qualyEntered = 0
    racesEntered = 0

    totalPoints = 0
    totalQualyPos = 0
    totalRacePos = 0


    #get all race results
    raceResults = requests.get(APILINK + f"session_result?driver_number={str(driver_number)}")

    #load as json
    racesJSON = json.loads(raceResults.content)

    for race in racesJSON: #iterate over each race

        sesKey = race["session_key"] #session key variable

        if not (race["dnf"] or race["dns"] or race["dsq"]): #avoid error if there is dnf/dns/dsq

            if sesKey in raceSessions: #if this race is in the raceID list

                totalPoints += race["points"] #add points to total
                totalRacePos += race["position"] #add to total race positions
                racesEntered += 1 #add 1 to races entered

            elif sesKey in qualySessions: #if is in qualy list
                totalQualyPos += race["position"] #add position to total qualy positions
                qualyEntered += 1 #add 1 to races entered

        else:
            if sesKey in raceSessions:
                totalRacePos += 20 #add last place to total
                racesEntered += 1

            elif sesKey in qualySessions:
                totalQualyPos += 20 #last place
                qualyEntered += 1


    #seperate variables for calculation
    raceCountCalc = racesEntered
    qualyCountCalc = qualyEntered

    #avoid division by 0
    if raceCountCalc == 0: raceCountCalc += 1
    if qualyCountCalc == 0: qualyCountCalc += 1 

    #calculate average
    averagePoints = totalPoints / raceCountCalc
    averageRacePos = totalRacePos / raceCountCalc
    averageQualyPos = totalQualyPos / qualyCountCalc

    #round results
    averagePoints = round(averagePoints, 2)
    averageRacePos = round(averageRacePos, 2)
    averageQualyPos = round(averageQualyPos, 2)

    return [racesEntered, averageRacePos, averagePoints, qualyEntered, averageQualyPos]