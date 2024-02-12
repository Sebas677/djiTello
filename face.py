from utils import *
import cv2

# Inicializamos y conectamos el dron
myDrone = initializeTello()
# Definimos el tamano de la imagen
w,h = 360,240
# Definimos valores de controlador
pid = [0.5 , 0, 0.5]
# Inicializamos variable de error
pError = 0
# Inicializamos una variable de vuelo
startCounter = 0
# Definimos las distancias a la que queremos que nos siga
fbRange = [6200, 6800]

while True:

    # Vuelo
    if startCounter == 0:
        myDrone.takeoff()
        startCounter = 1

    # Obtenemos la imagen de manera constante
    img = telloGetFrame(myDrone,w,h)
    # Obtenemos la imagen con la deteccion y el pixel central y el area del rostro detectado
    img, info = track_face_model(img)
    # Calculamos el error
    pError = trackFace(myDrone, info, w, pid, pError, fbRange)

    cv2.imshow("Image", img) # Mostramos la imagen obtenida

    # Esta parte permite interrumpir el codigo y aterrizar el dron
    if cv2.waitKey(1) & 0xFF == ord('q'):
        myDrone.land()
        break