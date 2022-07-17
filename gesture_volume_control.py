from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
import hand_tracking_module as htm
import numpy as np
import time
import cv2
import os
import sys
import math


#######################################################################
WIDTH, HEIGHT = 1280, 720
#######################################################################
cap = cv2.VideoCapture(0)
cap.set(3, WIDTH)
cap.set(4, HEIGHT)
p_time = 0
detector = htm.hand_detector()
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
vol_range = volume.GetVolumeRange()
min_volume_level = vol_range[0]
max_volume_level = vol_range[1]


while True:

    success, img = cap.read()
    img = detector.find_hands(img)
    lmList = detector.find_position(img, draw=False)

    if lmList is not None:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2) // 2, (y1+y2) // 2
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 69, 0), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        length = math.hypot((x2-x1), (y2-y1))
        vol_changer = np.interp(
            length, [50, 300], [min_volume_level, max_volume_level])
        print(vol_changer)
        volume.SetMasterVolumeLevel(vol_changer, None)

        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
        # Current sizes 50 - 300
        # Volume sizes -96 - 0

    c_time = time.time()
    fps = 1 / (c_time - p_time)
    p_time = c_time

    cv2.putText(img, f'FPS: {int(fps)}', (40, 70),
                cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 3)

    if success:
        cv2.imshow('IMG', img)
    cv2.waitKey(1)
