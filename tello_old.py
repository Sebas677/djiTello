from djitellopy import tello
import cv2
from time import sleep

me=tello.Tello()
me.connect()
print("battery: ",me.get_battery())

me.streamon()
cont=0
me.takeoff() 
me.send_rc_control(0, 0, 20, 0)
while True:
    img= me.get_frame_read().frame
    img= cv2.resize(img,(360,240)) 
    me.send_rc_control(5, 15, 0, 40)
    cv2.imshow("Image",img)

    # __________________________________________________EXIT COMMAND |SECTION
    if cv2.waitKey(1) == ord('q'):
        me.land()
        break
