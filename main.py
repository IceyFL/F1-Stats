#imports
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
    mainLoop = True
    while mainLoop: #loop until user exits program
        driversJSON = api.getDrivers() #load driver info

        for driver in driversJSON:
            print(f"{driver['driver_number']}  {driver['full_name']}")

        choice = intInput("Enter driver number: ", min = 1, max = 99) #get user input to get more info




#if this file is being run as main
if __name__ == "__main__":
    main()