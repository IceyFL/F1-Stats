#imports

#local imports
import api


#functions

#handle integer inputs
def intInput(message, min = None, max = None):
    valid = False
    while not valid: #loop until valid input given
        try:
            answer = int(input(message)) #get user input
            if (answer >= min or min == None) and (answer <= max or max == None): #check that input is between min and max if they are given
                valid = True #end loop
            else:
                print(f"Input must be between {str(min)} and {str(max)}")
        except ValueError: #prevent error if input is not an integer
            print("Input must be a number")

    return answer

#view stats of one driver
def driverStats(driversJSON):
    for driver in driversJSON: #output each drivers name and number
        print(f"{driver['driver_number']}  {driver['full_name']}")

    driverNum = intInput("Enter driver number: ", min = 1, max = 99) #get user input to get more info

    #get average points for that driver
    driverInfo = api.getSeasonInfo(driverNum)
    #driverInfo = [racesEntered, averageRacePos, averagePoints, dsqCount, qualyEntered, averageQualyPos, averageQualyGap]

    print("\nSeason Stats\n")
    print("Races entered: " + str(driverInfo[0]))
    print("DNF/DNS/DSQ count: " + str(driverInfo[3]))
    print("Average Result: " + str(driverInfo[1]))
    print("Average Points: " + str(driverInfo[2]))
    print("\nQualy Sessions Entered: " + str(driverInfo[4]))
    print("Average Qualy Result: " + str(driverInfo[5]))
    print("Average Qualy Gap: " + str(driverInfo[6]))

    input("\nPress enter to continue...\n")


#compare drivers
def compareDrivers(driversJSON):
    for driver in driversJSON: #output each drivers name and number
        print(f"{driver['driver_number']}  {driver['full_name']}")

    driver1 = intInput("Enter first driver number: ", min = 1, max = 99) #get user input to get more info
    driver2 = intInput("Enter second driver number: ", min = 1, max = 99) #get user input to get more info

    #get driver info
    driver1Info = api.getSeasonInfo(driver1)
    driver2Info = api.getSeasonInfo(driver2)
    #driverInfo = [racesEntered, averageRacePos, averagePoints, dsqCount, qualyEntered, averageQualyPos, averageQualyGap]

    #calculate differences
    DNFs = round(driver1Info[3] - driver2Info[3], 2)
    Results = round(driver1Info[1] - driver2Info[1], 2)
    Points = round(driver1Info[2] - driver2Info[2], 2)

    QualyResults = round(driver1Info[5] - driver2Info[5], 2)
    QualyGap = round(driver1Info[6] - driver2Info[6], 2)


    print(f"\nDriver {str(driver1)} vs Driver {str(driver2)}\n")
    print("DNF/DNS/DSQ Difference: " + str(DNFs))
    print("Average Result Difference: " + str(Results) + " Positions")
    print("Average Points Difference: " + str(Points) + " Points")
    print()
    print("Average Qualy Result Difference: " + str(QualyResults) + " Positions")
    print("Average Qualy Laptime Difference: " + str(QualyGap) + " Seconds")

    input("\nPress enter to continue...\n")


#main
def main():
    #get all drivers
    driversJSON = api.getDrivers() #load driver info

    mainLoop = True
    while mainLoop: #loop until user exits program
        #get user choice
        choice = intInput("\n1. See Driver Stats\n2. Compare Driver Stats\n", 1, 2)

        #choose what to do depending on user answer
        match choice:
            case 1: #view driver stats
                driverStats(driversJSON)
            case 2: #compare drivers
                compareDrivers(driversJSON)




#if this file is being run as main
if __name__ == "__main__":
    main()