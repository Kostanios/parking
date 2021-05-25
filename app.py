import os
from getNomer import get_nomer
from request import pushNomer
from _thread import start_new_thread
import datetime
# Specify device
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "true"

# Import all necessary libraries.
import numpy as np
import sys
import cv2

# NomeroffNet path
NOMEROFF_NET_DIR = os.path.abspath('../')

sys.path.append(NOMEROFF_NET_DIR)

# Import license plate recognition tools.
from NomeroffNet.YoloV5Detector import Detector
detector = Detector()
detector.load()

from NomeroffNet.BBoxNpPoints import NpPointsCraft
npPointsCraft = NpPointsCraft()
npPointsCraft.load()

from NomeroffNet.OptionsDetector import OptionsDetector
from NomeroffNet.TextDetector import TextDetector

from NomeroffNet import TextDetector

# load models
optionsDetector = OptionsDetector()
optionsDetector.load("latest")

textDetector = TextDetector.get_static_module("eu")()
textDetector.load("latest")

# Detect numberplate
img_path = 'public/images/people.jpg'
img = cv2.imread(img_path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

capture = cv2.VideoCapture('public/video/1.mp4')
previosCars = []

def searchMachine (previosCars):
    newCars = get_nomer(frame, detector=detector, npPointsCraft=npPointsCraft, optionsDetector=optionsDetector, textDetector=textDetector)
    if (newCars == None):
        newCars = []

    for previosCar in previosCars:
        if (previosCar not in newCars) & (len(previosCar) > 6):
            print('машина '+previosCar+'!')
            start_new_thread(pushNomer, (previosCar, datetime.date.today(), datetime.datetime.now().time(), ))
            
        else:
            print('машина не распознана')

    previosCars = newCars

while True:
    isTrue, frame = capture.read()
    cv2.imshow('video', frame)

    searchMachine(previosCars)

    if cv2.waitKey(20) & 0xFF == ord('d'):
        break




# ['JJF509', 'RP70012']