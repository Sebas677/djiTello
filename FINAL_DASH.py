# Python program to open the
# camera in Tkinter
# Import the libraries,
# tkinter, cv2, Image and ImageTk

from tkinter import *
import cv2 
from PIL import Image, ImageTk
from djitellopy import tello
import numpy as np
import random as rng
from ultralytics import YOLO
import time

# Define a video capture object
#vid = cv2.VideoCapture(0)

me=tello.Tello()
me.connect()
print("battery: ",me.get_battery())
battery=me.get_battery

me.streamon()
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

# Create a function to open camera and
# display it in the label_widget on app
# ____HULL |SECTION
def thresh_callback(val,src_gray):
    threshold = val
    # Detect edges using Canny
    canny_output = cv2.Canny(src_gray, threshold, threshold * 2)
    # Find contours
    contours, _ = cv2.findContours(canny_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Find the convex hull object for each contour
    hull_list = []
    for i in range(len(contours)):
        hull = cv2.convexHull(contours[i])
        hull_list.append(hull)
    # Draw contours + hull results
    drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
    for i in range(len(contours)):
        color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
        cv2.drawContours(drawing, contours, i, color)
        cv2.drawContours(drawing, hull_list, i, color)
    # Show in a window
    cv2.imshow('Contours', drawing)


def hull_camera():
    img= me.get_frame_read().frame
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    src_gray = cv2.GaussianBlur(gray, (5, 5), 0)
    blurred=src_gray

    # ____GRADIANT USING SOBEL |SECTION
    grad_x = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)

    # ____CALCULATE MAGNITUDE AND ANGLES |SECTION
    magnitude, angle = cv2.cartToPolar(grad_x, grad_y, angleInDegrees=True)

    # ____SUPRESSION|SECTION
    suppressed = cv2.dilate(cv2.erode(magnitude, None), None)
    magnitude = cv2.compare(magnitude, suppressed, cv2.CMP_EQ)

    # ____THRESHOLDS USE |SECTION
    threshold1, threshold2 = 50, 150
    edges = cv2.Canny(blurred, threshold1, threshold2)
    thresh=50
    # ____SHOW IMG|SECTION
    #cv.imshow("Image",edges)
    thresh_callback(thresh,src_gray)



def open_camera():
	# Capture the video frame by frame
	#_, frame = vid.read()
	
    frame= me.get_frame_read().frame
    frame=cv2.resize(frame,(100,100))

	# Convert image from one color space to other
    opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

	# Capture the latest frame and transform to image
    captured_image = Image.fromarray(opencv_image)

	# Convert captured image to photoimage
    photo_image = ImageTk.PhotoImage(image=captured_image)

	# Displaying photoimage in the label
    label_widget.photo_image = photo_image

	# Configure image in the label
    label_widget.configure(image=photo_image)

	# Repeat the same process after every 10 seconds
    label_widget.after(10, open_camera)


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
    while True:
        
        img = me.get_frame_read().frame
        me.send_rc_control(5, 15, 0, 40)
        cv2.imshow("Image",img)
        if cv2.waitKey(1) == ord('q'):
            me.land()
            break

#___________MODES

def vigilance_mode():
    me.send_rc_control(5, 15, 0, 40)

def canny_mode():
    while True:
        img= me.get_frame_read().frame
        frame= cv2.resize(img,(760,540))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Calculate the gradients using the Sobel operator
        grad_x = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)

        # Calculate the magnitude and direction of the edges
        magnitude, angle = cv2.cartToPolar(grad_x, grad_y, angleInDegrees=True)

        # Apply non-maximum suppression to the gradient magnitude
        suppressed = cv2.dilate(cv2.erode(magnitude, None), None)
        magnitude = cv2.compare(magnitude, suppressed, cv2.CMP_EQ)

        # Apply hysteresis thresholding to the image
        threshold1, threshold2 = 50, 150
        edges = cv2.Canny(blurred, threshold1, threshold2)

        cv2.imshow("Image",edges)
        if cv2.waitKey(1) == ord('q'):
            break


def yolo_mode_people():
    model = YOLO("yolov8n.pt")
    try:
        while True:
            #img= cv2.VideoCapture(0)
            img = me.get_frame_read().frame
            results = model.predict(img,classes=0, show=True)
            cv2.waitKey(1)
    except KeyboardInterrupt:
        exit(1)
    finally:
        print("End YOLO for people")

def yolo_mode_all():
    model = YOLO("yolov8n.pt")
    try:
        while True:
            #img= cv2.VideoCapture(0)
            img = me.get_frame_read().frame
            results = model.predict(img, show=True)
            cv2.waitKey(1)
    except KeyboardInterrupt:
        exit(1)
    finally:
        print("End YOLO for all")
    

app.columnconfigure((0, 1, 2, 3, 4, 5,6,7,8,9,10), weight=1)
app.rowconfigure((0, 1, 2, 3,4,5,6,7,8,9,10), weight=1)

# Create a label and display it on app
label_widget = Label(app)
label_widget.grid(column=4,row=2)
label_widget.config(background='gray')
   
# Create a button to open the camera in GUI app
button1 = Button(app, text="🎥", command=open_camera)
button1.grid(column=4, row=5)
#button1.configure(background='brown')

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


mode=Label(app, text="MODES")
mode.grid(column=0,row=7)

b_vigilance= Button(app, text="🧟",activebackground= "red", command=vigilance_mode)
b_vigilance.grid(column=2,row=7)

b_yolo= Button(app, text="👀",activebackground= "red", command=yolo_mode_all)
b_yolo.grid(column=3,row=7)

b_face= Button(app, text="😄",activebackground= "red", command=yolo_mode_people)
b_face.grid(column=4,row=7)

b_canny=Button(app, text="CANNY", command=canny_mode)
b_canny.grid(column=5,row=7)




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