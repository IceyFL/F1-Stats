#imports
import tkinter as tk
import requests
from os.path import exists

#local imports
import functions.api as api
import functions.gui as gui

#global variable
global selectedDrivers
selectedDrivers = [None, None]

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


#download driver image
def downloadDriverImage(headshotUrl, driverNumber):
    fileName = f"driverImages/{str(driverNumber)}.png"
    if not exists(fileName): #image dosnt already exist
        if headshotUrl != None: #headshot url exists
            with open(fileName, 'wb') as f: #open image
                f.write(requests.get(headshotUrl).content) #write image


def main():
    #setup window for the UI
    root = tk.Tk()
    root.title("F1 Stats")
    root.resizable(False, False)
    root.protocol("WM_DELETE_WINDOW", exit) #close program when window closes

    #get json data on all drivers that competed in the last session
    driversJSON = api.getDrivers()
    #sort drivers by team
    driversJSON = sorted(driversJSON, key=lambda d: d["team_colour"], reverse=True)

    #create UI grid sectors
    (main_frame, left_panel, grid_frame_left, middle_panel, grid_frame_right, right_panel) = gui.createGrid(root)
    textPanels = [left_panel, middle_panel, right_panel]

    #initialize drivers list
    drivers = []
    for i, driver in enumerate(driversJSON): #iterate through all drivers
        #add driver to drivers list
        drivers.append([driver["driver_number"], driver["full_name"], "#" + driver["team_colour"]])

        #make sure drivers image is downloaded
        downloadDriverImage(driver["headshot_url"], drivers[i][0])

        #create button on UI for driver
        target_frame = grid_frame_left if (i // 2) % 2 == 0 else grid_frame_right # Alternate drivers between left and right grid
        gui.createDriverButton(textPanels, target_frame, i, drivers[-1], drivers[i][0], drivers[i][1], drivers[i][2], showDriverStats,)

    root.mainloop()


#show driver stats if drivers button is clicked
def showDriverStats(driver, textPanels):
    global selectedDrivers
    #assign variable as global so it can be modified    

    #check if there is already drivers on the comparison
    if selectedDrivers[0] == None: #comparison slot 1
        #get drivers stats for the season
        driverStats = api.getSeasonInfo(driver[0])
        
        #add driver to panel
        gui.driverPanel(textPanels[0], driver, driverStats, clearDriver, textPanels[1])

        #add driver to selected drivers list
        selectedDrivers[0] = driver

        if selectedDrivers[1] != None: #selected drivers list full
            #get driver stats
            driver2Stats = api.getSeasonInfo(selectedDrivers[1][0])

            #add comparison box to middle panel
            gui.middlePanel(textPanels[1], driverStats, driver2Stats)


    elif selectedDrivers[1] == None: #comparison slot 2
        #get drivers stats for the season
        driverStats = api.getSeasonInfo(driver[0])

        #add driver to panel
        gui.driverPanel(textPanels[2], driver, driverStats, clearDriver, textPanels[1])

        #add driver to selected drivers list
        selectedDrivers[1] = driver

        #get other driver stats
        driver1Stats = api.getSeasonInfo(selectedDrivers[0][0])

        #add comparison box in the middle
        gui.middlePanel(textPanels[1], driver1Stats, driverStats)



#if clear button is clicked
def clearDriver(panel, middlePanel):
    global selectedDrivers
    #allow selecteddrivers to be modified

    gui.clearPanel(panel)
    gui.clearPanel(middlePanel)

    # Reset the correct side in selectedDrivers
    if panel.winfo_name() == "left_panel":
        selectedDrivers[0] = None
    elif panel.winfo_name() == "right_panel":
        selectedDrivers[1] = None




#if this file is being run as main
if __name__ == "__main__":
    main()