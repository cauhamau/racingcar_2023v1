from client_lib import GetStatus,GetRaw,GetSeg,AVControl,CloseSocket

import cv2
import numpy as np

import copy

import torch
import time


from src import util
from net import Net
net = Net()
net.load_model(49,"0.2270")


MAX_SPEED = 20
MAX_ANGLE = 25
Min_SPEED = 10

global sendBack_angle, sendBack_Speed, current_speed, current_angle
sendBack_angle = 0
sendBack_Speed = 0
current_speed = 0
current_angle = 0

if __name__ == "__main__":
    print('Wait a minutes')
    #try:
    while True:
        state = GetStatus()
        image = GetRaw()
        #segment_image = GetSeg()
        key = cv2.waitKey(1)
        #print(state)
        #cv2.imshow('segment_image', segment_image)
        
        # maxspeed = 90, max steering angle = 25
        AVControl(speed=sendBack_Speed, angle=sendBack_angle)



        #try:
        #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image,(512,256))


        x, y = net.predict(image)
        print("---------x-----------")
        print(x)
        fits = np.array([np.polyfit(_y, _x, 1) if len(_x) < 5  else  np.polyfit(_y, _x, 2) for _x, _y in zip(x, y)])
        fits = np.array([np.polyfit(_y, _x, 1) for _x, _y in zip(x, y)])
        
        sendBack_angle = util.get_steer_angle(fits, current_speed)
        
        print(f"Angle:{sendBack_angle}")
        print(f"len_fit:{fits.shape[0]}")
        
        
        if sendBack_Speed > MAX_SPEED:
            sendBack_Speed = 5
        if sendBack_Speed < Min_SPEED:
            sendBack_Speed = 35
        
        
        # except Exception as er:
        #     pass
        cv2.imshow('raw_image', image)
        if key == ord('q'):
            break

    # finally:
    #     print('closing socket')
    #     CloseSocket()

