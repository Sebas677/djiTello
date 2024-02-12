from djitellopy import tello
import numpy as np
import pathlib
import cv2

def initializeTello():
    # Iniciamos conexion con el dron, definimos en 0 las velocidades, desconectamos y conectamos al camara por temas de seguridad.
    myDrone = tello.Tello()
    myDrone.connect()
    myDrone.send_rc_control(0,0,0,0)
    print(myDrone.get_battery())
    myDrone.streamoff()
    myDrone.streamon()
    return myDrone

def telloGetFrame(myDrone, w= 360, h=240):
    # Comenzamos a obtener el video del dron
    myFrame = myDrone.get_frame_read()
    myFrame = myFrame.frame
    img = cv2.resize(myFrame,(w,h))
    return img

def track_face_model(img):
    # Buscamos en que direccion se encuentra el modelo para detectar rostros
    clf = cv2.CascadeClassifier("haarcascade-frontalface-default.xml")
    # Convertimos la imagen a escala de grises
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # Detectamos los rostros utilizando el modelo en la imagen a escala de grises
    faces = clf.detectMultiScale(imgGray,1.2,8)

    # Creamos 2 listas
    myFaceListC = []
    myFaceListArea = []

    # Por cada deteccion obtener las coordenadas x, y, w y h, ademas de imprimir la bounding box en la imagen
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        # Obtenemos el pixel central en x y y
        cx = x + (w // 2)
        cy = y + (h // 2)
        cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        # Calculamos el area de la bounding box
        area = w*h
        # Almacenamos los datos calculados en listas
        myFaceListArea.append(area)
        myFaceListC.append([cx,cy])

    # Si el tamano de la lista es distinto de 0
    if len(myFaceListArea) !=0:
        # i va a valer el indice maximo de la lista myFaceListArea
        i = myFaceListArea.index(max(myFaceListArea))
        # Regresamos la imagen y los valores de la lista del indice maximo de las listas
        return img, [myFaceListC[i],myFaceListArea[i]]
    # En cualquier otro caso enviamos la imagen y 0 en los valores
    else:
        return img,[[0,0],0]
    
def trackFace(myDrone,info,w,pid,pError,fbRange):

    # PID
    area = info[1]
    x, y = info[0]
    fb = 0
    
    error = x - w//2
    speed = pid[0]*error + pid[1]*sum(pError) + pid[2]*(error-pError)
    speed = np.clip(speed,-100,100)

    if area > fbRange[0] and area < fbRange[1]:
        fb = 0
    elif area > fbRange[1]:
        fb = -20
    elif area < fbRange[0] and area != 0 :
        fb = 20

    if x == 0:
        speed = 0
        error = 0

    myDrone.send_rc_control(0,fb,0,speed)

    return error


