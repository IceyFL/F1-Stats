#imports
import tkinter as tk


#functions

#create UI sections
def createGrid(root):
    # Create main layout frame
    main_frame = tk.Frame(root)
    main_frame.pack()

    # Left stats panel (Driver 1)
    left_panel = tk.Frame(main_frame, width=200, height=575, bg="white", name="left_panel")
    left_panel.grid(row=0, column=0)
    left_panel.pack_propagate(False)

    # Driver grid container
    grid_frame_left = tk.Frame(main_frame)
    grid_frame_left.grid(row=0, column=1, padx=5, pady=5)

    # Comparison panel
    middle_panel = tk.Frame(main_frame, width=200, height=575, bg="white")
    middle_panel.grid(row=0, column=2)
    middle_panel.pack_propagate(False)

    # Driver grid container
    grid_frame_right = tk.Frame(main_frame)
    grid_frame_right.grid(row=0, column=3, padx=5, pady=5)

    # Right stats panel (Driver 2)
    right_panel = tk.Frame(main_frame, width=200, height=575, bg="white", name="right_panel")
    right_panel.grid(row=0, column=4)
    right_panel.pack_propagate(False)

    return (main_frame, left_panel, grid_frame_left, middle_panel, grid_frame_right, right_panel)

#add drivers button to the UI
def createDriverButton(textPanels, grid_frame, i, driver, driver_number, full_name, team_colour, buttonFunction):

    card = tk.Frame(grid_frame, width=130, height=110) #create a card to put the image and text on
    card.grid(row=i // 4, column=i % 4, padx=5, pady=5) #set grid and collumn
    card.pack_propagate(False) #stop auto resize

    # add background colour
    canvas = tk.Canvas(card, width=130, height=110, bg=team_colour, highlightthickness=0)
    canvas.pack()

    # Load image
    img_path = f"driverImages/{driver_number}.png" #image path
    try:
        photo = tk.PhotoImage(file=img_path)
    except Exception: #catch error if image dosnt exist
        photo = None

    if photo: #if image exists
        canvas.create_image(15, 0, image=photo, anchor="nw")
        canvas.image = photo  # Keep reference

    # Black background at bottom so text is always clear
    canvas.create_rectangle(0, 90, 130, 110, fill="black", outline="black")
    # add text
    canvas.create_text(65, 100, text=full_name, fill="white", font=("Arial", 9, "bold"))

    # Make canvas clickable
    canvas.bind("<Button-1>", lambda e, d=driver: buttonFunction(d, textPanels))


#create driver panel
def driverPanel(panel, driver, driverStats, clearFunction, middlePanel):
    # load driver image
    img_path = f"driverImages/{str(driver[0])}.png"
    try:
        photo = tk.PhotoImage(file=img_path).zoom(2,2) #load image and double its size
        image_label = tk.Label(panel, image=photo, bg=driver[2]) #set background of image to team color
        image_label.image = photo  # Keep reference to prevent garbage collection
        image_label.pack(pady=10)
    except Exception: #catch error if image dosnt exist
        pass

    # Create stats text
    stats_text = (
        f"Races Entered: {driverStats[0]}\n"
        f"DNF Count: {driverStats[3]}\n"
        f"Average Result: {driverStats[1]:.2f}\n"
        f"Average Points: {driverStats[2]:.2f}\n\n"
        f"Qualy Sessions Entered: {driverStats[4]}\n"
        f"Average Qualy Result: {driverStats[5]:.2f}\n"
        f"Average Qualy Gap: {driverStats[6]:.3f}s"
    )

    # Display stats
    stats_label = tk.Label(panel, text=stats_text, bg="white", font=("Arial", 9, "bold"), justify="left")
    stats_label.pack(pady=(0, 10))

    # Add "Clear" button at the bottom
    clear_button = tk.Button(panel, text="Clear", command=lambda: clearFunction(panel, middlePanel), width=20)
    clear_button.pack(pady=10)


#create comparison panel
def middlePanel(panel, driver1Stats, driver2Stats):
    # Calculate differences and format them
    comparison_text = (
        f"Race Comparison:\n"
        f"Races Difference: {driver2Stats[0] - driver1Stats[0]}\n"
        f"DNF Difference: {driver2Stats[3] - driver1Stats[3]}\n"
        f"Avg Result Difference: {driver2Stats[1] - driver1Stats[1]:+.2f}\n"
        f"Avg Points Difference: {driver2Stats[2] - driver1Stats[2]:+.2f}\n\n"
        f"Qualifying Comparison:\n"
        f"Sessions Difference: {driver2Stats[4] - driver1Stats[4]}\n"
        f"Avg Qualy Pos Difference: {driver2Stats[5] - driver1Stats[5]:+.2f}\n"
        f"Avg Qualy Gap Difference: {driver2Stats[6] - driver1Stats[6]:+.3f}s"
    )

    # Display comparison
    comparison_label = tk.Label(panel, text=comparison_text, bg="white", font=("Arial", 9, "bold"), justify="left")
    comparison_label.pack(pady=20)


#clear panel
def clearPanel(panel):
    for widget in panel.winfo_children():
        widget.destroy()