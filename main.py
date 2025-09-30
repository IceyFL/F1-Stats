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


#main
def main():
    #get all drivers
    driversJSON = api.getDrivers() #load driver info

    mainLoop = True
    while mainLoop: #loop until user exits program
        for driver in driversJSON: #output each drivers name and number
            print(f"{driver['driver_number']}  {driver['full_name']}")

        driverNum = intInput("Enter driver number: ", min = 1, max = 99) #get user input to get more info

        #get average points for that driver
        driverInfo = api.getSeasonInfo(driverNum)
        #driverInfo = [RacesEntered, AveragePoints]

        print("Races entered: " + str(driverInfo[0]))
        print("Average Points: " + str(driverInfo[1]))

        input("\nPress enter to continue...\n")




#if this file is being run as main
if __name__ == "__main__":
    main()