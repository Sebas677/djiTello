from tkinter import *
import cv2
from PIL import Image, ImageTk
from djitellopy import tello
import threading
import time

# Initialize the Tello drone
me = tello.Tello()

# Connect to the Tello drone
me.connect()
print("Battery: ", me.get_battery())

# Set speed for the joypad controls
speed = 20
me.streamon()

# Declare the width and height in variables
width, height = 500, 600

# Create a GUI app
app = Tk()

# Bind the app with Escape keyboard to quit app whenever pressed
app.bind('<Escape>', lambda e: app.quit())

# Create a label to display the video feed
label_widget = Label(app)
label_widget.grid(column=0, row=0, columnspan=4)

# Function to update the video feed label with new frames
def update_frame():
    while True:
        frame = me.get_frame_read().frame
        frame = cv2.resize(frame, (760, 540))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(Image.fromarray(frame))
        label_widget.imgtk = img
        label_widget.configure(image=img)
        label_widget.after(10, update_frame)

# Function to continuously send movement commands to the Tello drone
def send_movement_commands():
    while True:
        if movement_command is not None:
            me.send_rc_control(*movement_command)
            time.sleep(0.5)
        else:
            time.sleep(0.1)

# Thread for updating the video feed
video_thread = threading.Thread(target=update_frame)
video_thread.daemon = True
video_thread.start()

# Thread for sending movement commands
movement_thread = threading.Thread(target=send_movement_commands)
movement_thread.daemon = True
movement_thread.start()

# Variables for movement commands
movement_command = None

# Functions to control the Tello drone
def control_TAKEOFF():
    global movement_command
    movement_command = (0, 0, speed, 0)
    me.takeoff()

def control_LAND():
    global movement_command
    movement_command = (0, 0, -speed, 0)
    me.land()

def control_LEFT():
    global movement_command
    movement_command = (-speed, 0, 0, 0)

def control_RIGHT():
    global movement_command
    movement_command = (speed, 0, 0, 0)

def control_UP():
    global movement_command
    movement_command = (0, 0, speed, 0)

def control_DOWN():
    global movement_command
    movement_command = (0, 0, -speed, 0)

def control_turnLeft():
    global movement_command
    movement_command = (0, 0, 0, -speed)

def control_turnRight():
    global movement_command
    movement_command = (0, 0, 0, speed)

def control_front():
    global movement_command
    movement_command = (0, speed, 0, 0)

def control_back():
    global movement_command
    movement_command = (0, -speed, 0, 0)

# Functions for YOLO modes
def yolo_mode_all():
    # Implement your YOLO mode for all objects detection
    pass

def yolo_mode_people():
    # Implement your YOLO mode for people detection
    pass

# Function for Canny mode
def canny_mode():
    # Implement your Canny mode
    pass

# Create buttons for drone movement
button1 = Button(app, text="Takeoff", command=control_TAKEOFF)
button1.grid(column=0, row=1)

button2 = Button(app, text="Land", command=control_LAND)
button2.grid(column=1, row=1)

button3 = Button(app, text="Left", command=control_LEFT)
button3.grid(column=0, row=2)

button4 = Button(app, text="Right", command=control_RIGHT)
button4.grid(column=1, row=2)

button5 = Button(app, text="Up", command=control_UP)
button5.grid(column=0, row=3)

button6 = Button(app, text="Down", command=control_DOWN)
button6.grid(column=1, row=3)

button7 = Button(app, text="Turn Left", command=control_turnLeft)
button7.grid(column=0, row=4)

button8 = Button(app, text="Turn Right", command=control_turnRight)
button8.grid(column=1, row=4)

button9 = Button(app, text="Front", command=control_front)
button9.grid(column=0, row=5)

button10 = Button(app, text="Back", command=control_back)
button10.grid(column=1, row=5)

# Create buttons for YOLO modes
b_yolo_all = Button(app, text="👀", command=yolo_mode_all)
b_yolo_all.grid(column=1, row=7)

b_yolo_people = Button(app, text="😄", command=yolo_mode_people)
b_yolo_people.grid(column=2, row=7)

# Create a button for Canny mode
b_canny = Button(app, text="☃", command=canny_mode)
b_canny.grid(column=3, row=7)

# Start the GUI app
app.mainloop()
