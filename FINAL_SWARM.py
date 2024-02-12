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

# Define a video capture object
#vid = cv2.VideoCapture(0)

me=tello.Tello()

me = TelloSwarm.fromIps([
    "192.168.137.103",
    "192.168.137.149",
    "192.168.137.237",
    "192.168.137.175"
])
me.connect()
print("battery: ",me.get_battery())
battery=me.get_battery

speed=20

# Declare the width and height in variables
width, height = 500, 600

#img= me.get_frame_read().frame
#img= cv2.resize(img,(width,height))


# Create a GUI app
app = Tk()

# Bind the app with Escape keyboard to
# quit app whenever pressed
app.bind('<Escape>', lambda e: app.quit())
app.title ('Tello Talent')
app.geometry('400x350')
app.config (background='gray')



#____EXECUTE
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

#____TRAJECTORIES
def line_traj():
    # Move forward for 50 cm
    print("Has escogido una trayectoria en linea")
    print("Ingrese la distancia que desea recorrer (cm)")
    distancia = int(input())
    me.send_rc_control(0,distancia,0,0)
    #me.move_forward(distancia)
    time.sleep(3)
    print("La distancia que recorrio fue de:" + distancia + "cm" )

def triangle_traj():

    print("Has escogido una trayectoria en forma triangular (Equilatero)")
    print("Ingrese la distancia del triangulo (cm)")
    distancia = int(input())
    # Move forward for 50 cm
    me.move_forward(distancia)
    time.sleep(3)
    # Rotate clockwise by 90 degrees
    me.rotate_clockwise(60)
    time.sleep(3)

    # Move forward for 50 cm
    me.move_forward(distancia)
    time.sleep(3)
    # Rotate clockwise by 90 degrees
    me.rotate_clockwise(60)
    time.sleep(3)

     # Move forward for 50 cm
    me.move_forward(distancia)
    time.sleep(3)
    # Rotate clockwise by 90 degrees
    me.rotate_clockwise(60)
    time.sleep(3)
    print("La distancia del triangulo fue de:" + distancia + "cm" )

def hexagon_traj():
    print("Has escogido una trayectoria en forma hexagonal (Equilatero)")
    print("Ingrese la distancia del hexagono (cm)")
    distancia = int(input())
    # Move forward for 50 cm
    me.move_forward(distancia)
    time.sleep(3)
    # Rotate clockwise by 90 degrees
    me.rotate_clockwise(120)
    time.sleep(3)

    # Move forward for 50 cm
    me.move_forward(distancia)
    time.sleep(3)
    # Rotate clockwise by 90 degrees
    me.rotate_clockwise(120)
    time.sleep(3)

     # Move forward for 50 cm
    me.move_forward(distancia)
    time.sleep(3)
    # Rotate clockwise by 90 degrees
    me.rotate_clockwise(120)
    time.sleep(3)

    # Move forward for 50 cm
    me.move_forward(distancia)
    time.sleep(3)
    # Rotate clockwise by 90 degrees
    me.rotate_clockwise(120)
    time.sleep(3)

    # Move forward for 50 cm
    me.move_forward(distancia)
    time.sleep(3)
    # Rotate clockwise by 90 degrees
    me.rotate_clockwise(120)
    time.sleep(3)

    # Move forward for 50 cm
    me.move_forward(distancia)
    time.sleep(3)
    # Rotate clockwise by 90 degrees
    me.rotate_clockwise(120)
    time.sleep(3)
    print("La distancia del hexagono fue de:" + distancia + "cm" ) 

def square_traj():
    print("Has escogido una trayectoria del cuadrado (Equilatero)")
    print("Ingrese la distancia del cuadrado (cm)")
    distancia = int(input())
    # Move forward for 50 cm
    me.move_forward(distancia)
    time.sleep(3)
    # Rotate clockwise by 90 degrees
    me.rotate_clockwise(90)
    time.sleep(3)

    # Move forward for 50 cm
    me.move_forward(distancia)
    time.sleep(3)
    # Rotate clockwise by 90 degrees
    me.rotate_clockwise(90)
    time.sleep(3)

     # Move forward for 50 cm
    me.move_forward(distancia)
    time.sleep(3)
    # Rotate clockwise by 90 degrees
    me.rotate_clockwise(90)
    time.sleep(3)

    # Move forward for 50 cm
    me.move_forward(distancia)
    time.sleep(3)
    # Rotate clockwise by 90 degrees
    me.rotate_clockwise(90)
    time.sleep(3)
    print("La distancia del cuadrado fue de:" + distancia + "cm" ) 

def circle_traj():
     me.send_rc_control(5, 15, 0, 40)
     time.sleep(15)
    

#___________MODES



app.columnconfigure((0, 1, 2, 3, 4, 5,6,7,8,9,10), weight=1)
app.rowconfigure((0, 1, 2, 3,4,5,6,7,8,9,10), weight=1)

# Create a label and display it on app
label_widget = Label(app)
label_widget.grid(column=4,row=2)
label_widget.config(background='gray')
   

# Create a button to open the camera in GUI app
button2 = Button(app, text="≙",activebackground= "red", command=control_TAKEOFF) #activebackground= "red"
button2.grid(column=3, row=5)



# Create a button to open the camera in GUI app
button3 = Button(app, text="≚",activebackground= "red", command=control_LAND)
button3.grid(column=5, row=5)

# Create a button to open the camera in GUI app
button4 = Button(app, text="≪",activebackground= "red", command=control_LEFT)
button4.grid(column=1, row=2)
time.sleep(0.5)

# Create a button to open the camera in GUI app
button5 = Button(app, text="≫",activebackground= "red", command=control_RIGHT)
button5.grid(column=3, row=2)
time.sleep(0.5)

# Create a button to open the camera in GUI app
button6 = Button(app, text="⊼",activebackground= "red", command=control_front)
button6.grid(column=2, row=1)
time.sleep(0.5)

# Create a button to open the camera in GUI app
button7 = Button(app, text="⊽",activebackground= "red", command=control_back)
button7.grid(column=2, row=3)
time.sleep(0.5)

# Create a button to open the camera in GUI app
button8 = Button(app, text="↥",activebackground= "red", command=control_UP)
button8.grid(column=6, row=1)
time.sleep(0.5)

# Create a button to open the camera in GUI app
button9 = Button(app, text="↧",activebackground= "red", command=control_DOWN)
button9.grid(column=6, row=3)
time.sleep(0.5)

# Create a button to open the camera in GUI app
button9 = Button(app, text="⟲",activebackground= "red", command=control_turnLeft)
button9.grid(column=5, row=2)
time.sleep(0.5)

# Create a button to open the camera in GUI app
button9 = Button(app, text="⟳",activebackground= "red", command=control_turnRight)
button9.grid(column=7, row=2)
time.sleep(0.5)


div0=Label(app,text=" ")
div0.grid(column=4, row=6)
div0.config(background='gray')
div1=Label(app,text=" ")
div1.grid(column=8, row=6)
div1.config(background='gray')



traj=Label(app, text="TRAJEC")
traj.grid(column=0,row=9)

line= Button(app, text="│",activebackground= "red", command=line_traj)
line.grid(column=1,row=9)

triang= Button(app, text="△",activebackground= "red", command=triangle_traj)
triang.grid(column=2,row=9)

hex= Button(app, text="⎔",activebackground= "red", command=hexagon_traj)
hex.grid(column=3,row=9)

square= Button(app, text="☐",activebackground= "red", command=square_traj)
square.grid(column=4,row=9)

circle= Button(app, text="⊙",activebackground= "red", command=circle_traj)
circle.grid(column=5,row=9)


# Create an infinite loop for displaying app on screen
app.mainloop()