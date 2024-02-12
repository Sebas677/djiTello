# Python program to open the
# camera in Tkinter
# Import the libraries,
# tkinter, cv2, Image and ImageTk

from tkinter import *
import cv2 
from PIL import Image, ImageTk
from djitellopy import tello, TelloSwarm
import numpy as np
import random as rng
from ultralytics import YOLO
import time

me=tello.Tello()

me.connect()
print("battery: ",me.get_battery())


#set speed fot the joypad controls
speed=20
me.streamon()
# Declare the width and height in variables
width, height = 500, 600

# Create a GUI app
app = Tk()

# Bind the app with Escape keyboard to
# quit app whenever pressed
app.bind('<Escape>', lambda e: app.quit())

def open_camera():
    while True:
        img= me.get_frame_read().frame
        frame= cv2.resize(img,(760,540))
        cv2.imshow("Image",frame)
        if cv2.waitKey(1) == ord('q'):
            break

#________EXECUTE
def control_TAKEOFF():
    me.takeoff()
def control_LAND():
    me.land()

#________CONTROL  
def control_LEFT():
    me.send_rc_control(-speed,0,0,0)
    time.sleep(0.5)
def control_RIGHT():
    me.send_rc_control(speed,0,0,0)
    time.sleep(0.5)
def control_UP():
    me.send_rc_control(0,0,speed,0)
    time.sleep(0.5)
def control_DOWN():
    me.send_rc_control(0,0,-speed,0)
    time.sleep(0.5)
def control_turnLeft():
    me.send_rc_control(0,0,0,-speed)
    time.sleep(0.5)
def control_turnRight():
    me.send_rc_control(0,0,0,speed)
    time.sleep(0.5)
def control_front():
    me.send_rc_control(0,speed,0,0)
    time.sleep(0.5)
def control_back():
    me.send_rc_control(0,-speed,0,0)
    time.sleep(0.5)

#________TRAJECTORIES
def line_traj():
    distance = int(input())
    me.send_rc_control(0,distance,0,0)
    time.sleep(3)

def triangle_traj():

    distance = int(input())

    me.move_forward(distance)
    time.sleep(3)
    # Rotate clockwise by 60 degrees
    me.rotate_clockwise(60)
    time.sleep(3)

    me.move_forward(distance)
    time.sleep(3)
    # Rotate clockwise by 60 degrees
    me.rotate_clockwise(60)
    time.sleep(3)

    me.move_forward(distance)
    time.sleep(3)
    # Rotate clockwise by 60 degrees
    me.rotate_clockwise(60)
    time.sleep(3)


def hexagon_traj():

    distance = int(input())

    me.rotate_clockwise(300)
    time.sleep(2)
    me.move_forward(distance)
    time.sleep(2)
    me.rotate_clockwise(90)
    time.sleep(2)
    me.move_forward(distance)
    time.sleep(2)
    me.rotate_clockwise(60)
    time.sleep(2)
    me.move_forward(distance)
    time.sleep(2)
    me.rotate_clockwise(60)
    time.sleep(2)
    me.move_forward(distance)
    time.sleep(2)
    me.rotate_clockwise(60)
    time.sleep(2)
    me.move_forward(distance)
    time.sleep(2)
    me.rotate_clockwise(70)
    time.sleep(2)
    me.move_forward(distance)
    time.sleep(2)
    me.rotate_clockwise(90)

def square_traj():

    distance = int(input())

    me.move_forward(distance)
    time.sleep(3)
    # Rotate clockwise by 90 degrees
    me.rotate_clockwise(90)
    time.sleep(3)


    me.move_forward(distance)
    time.sleep(3)
    # Rotate clockwise by 90 degrees
    me.rotate_clockwise(90)
    time.sleep(3)

    me.move_forward(distance)
    time.sleep(3)
    # Rotate clockwise by 90 degrees
    me.rotate_clockwise(90)
    time.sleep(3)

    me.move_forward(distance)
    time.sleep(3)
    # Rotate clockwise by 90 degrees
    me.rotate_clockwise(90)
    time.sleep(3)


def circle_traj():        
    me.send_rc_control(5, 15, 0, 40)
    time.sleep(10)


#___________________________MODES
def canny_mode():
    while True:
        img= me.get_frame_read().frame
        frame= cv2.resize(img,(760,540))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Apply hysteresis thresholding to the image
        threshold1, threshold2 = 50, 150
        edges = cv2.Canny(blurred, threshold1, threshold2)

        cv2.imshow("Image",edges)
        if cv2.waitKey(1) == ord('q'):
            break

def yolo_mode_people():
    model = YOLO("yolov8n.pt")
    while True:
        #img= cv2.VideoCapture(0)
        img = me.get_frame_read().frame
        results = model.predict(img,classes=0, show=True)
        if cv2.waitKey(1) == ord('q'):
            break
    

def yolo_mode_all():
    model = YOLO("yolov8n.pt")
    while True:
        #img= cv2.VideoCapture(0)
        img = me.get_frame_read().frame
        results = model.predict(img, show=True)
        if cv2.waitKey(1) == ord('q'):
            break
 
app.columnconfigure((0, 1, 2, 3, 4, 5,6,7,8,9,10), weight=1)
app.rowconfigure((0, 1, 2, 3,4,5,6,7,8,9,10), weight=1)

# Create a label and display it on app
label_widget = Label(app)
label_widget.grid(column=4,row=2)
   
# Create a button to open the camera in GUI app
button1 = Button(app, text="🎥", command=open_camera)
button1.grid(column=4, row=5)

# Create a button to takeoff in GUI app
button2 = Button(app, text="≙",activebackground= "red", command=control_TAKEOFF) #activebackground= "red"
button2.grid(column=3, row=5)


# Create a button to land in GUI app
button3 = Button(app, text="≚",activebackground= "red", command=control_LAND)
button3.grid(column=5, row=5)

# Create a button to move to the left in GUI app
button4 = Button(app, text="≪",activebackground= "red", command=control_LEFT)
button4.grid(column=1, row=2)
time.sleep(0.5)

# Create a button to move to the right in GUI app
button5 = Button(app, text="≫",activebackground= "red", command=control_RIGHT)
button5.grid(column=3, row=2)
time.sleep(0.5)

# Create a button to go forward in GUI app
button6 = Button(app, text="⊼",activebackground= "red", command=control_front)
button6.grid(column=2, row=1)
time.sleep(0.5)

# Create a button to go backward in GUI app
button7 = Button(app, text="⊽",activebackground= "red", command=control_back)
button7.grid(column=2, row=3)
time.sleep(0.5)

# Create a button to ascend in GUI app
button8 = Button(app, text="↥",activebackground= "red", command=control_UP)
button8.grid(column=6, row=1)
time.sleep(0.5)

# Create a button to descend GUI app
button9 = Button(app, text="↧",activebackground= "red", command=control_DOWN)
button9.grid(column=6, row=3)
time.sleep(0.5)

# Create a button to rotate counter-clockwise in GUI app
button10 = Button(app, text="⟲",activebackground= "red", command=control_turnLeft)
button10.grid(column=5, row=2)
time.sleep(0.5)

# Create a button to rotate clockwise in GUI app
button11 = Button(app, text="⟳",activebackground= "red", command=control_turnRight)
button11.grid(column=7, row=2)
time.sleep(0.5)



div0=Label(app,text=" ")
div0.grid(column=4, row=6)
div1=Label(app,text=" ")
div1.grid(column=8, row=6)

mode=Label(app, text="MODES")
mode.grid(column=0,row=7)

b_yolo= Button(app, text="👀", command=yolo_mode_all)
b_yolo.grid(column=1,row=7)

b_face= Button(app, text="😄", command=yolo_mode_people)
b_face.grid(column=2,row=7)

b_solo= Button(app, text="☃", command=canny_mode)
b_solo.grid(column=3,row=7)



traj=Label(app, text="TRAJEC")
traj.grid(column=0,row=9)

line= Button(app, text="│", command=line_traj)
line.grid(column=1,row=9)

triang= Button(app, text="△", command=triangle_traj)
triang.grid(column=2,row=9)

hex= Button(app, text="⎔", command=hexagon_traj)
hex.grid(column=3,row=9)

square= Button(app, text="☐", command=square_traj)
square.grid(column=4,row=9)

circle= Button(app, text="⊙", command=circle_traj)
circle.grid(column=5,row=9)




# Create an infinite loop for displaying app on screen
app.mainloop()