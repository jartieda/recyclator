from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import requests
import sys
from gpiozero import LED, Button
from signal import pause

# This function will pass your image to the machine learning model
# and return the top result with the highest confidence
def classify(imagefile):
    key = "<yourkey>"
    url = "https://gateway.watsonplatform.net/visual-recognition/api/v3/classify?version=2018-03-19"
    response = requests.post(url, files={'file':open(imagefile,'rb')},
                             data={"threshold": 0.5,
                                   "classifier_ids":"recyclator_1982716980"},
                             auth=('apikey',key))
    if response.ok:
        responseData = response.json()
        #print ("resultado: ", responseData)
        topMatch = responseData['images'][0]['classifiers'][0]['classes'][0]
        return topMatch
    else:
        response.raise_for_status()


# CHANGE THIS to the name of the image file you want to classify
#inicia la camara
camera = PiCamera()
rawCapture = PiRGBArray(camera)
time.sleep(0.1)
button = Button(9)
led_blue = LED(5)
led_yellow = LED(6)
led_red = LED(13)
led_green = LED(19)
led_white = LED(26)
while True:
    button.wait_for_press()
    led_blue.off()
    led_yellow.off()
    led_red.off()
    led_green.off()
    led_white.off()

    #guarda la imagen
    camera.capture('/home/pi/Desktop/image.jpg')

    demo = classify("/home/pi/Desktop/image.jpg")

    label = demo["class"]
    confidence = demo["score"]*100


    # CHANGE THIS to do something different with the result
    print ("result: '%s' with %d%% confidence" % (label, confidence))
    if label == "paper":
        print("blue")
        led_blue.on()
    elif label == "envases":
        print("yelllow")
        led_yellow.on()
    elif label == "glass":
        print("green")
        led_green.on()
    elif label == "organic":
        print("red")
        led_red.on()
    else:
        print("white")
        led_white.on()
