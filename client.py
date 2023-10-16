
import socket
import cv2
import numpy as np

import copy

import torch
import time


from src import util
from net import Net
net = Net()

SetStatusObjs = []
StatusLines = []
StatusBoxes = []


MAX_SPEED = 35
MAX_ANGLE = 25

speed_limit = MAX_SPEED
MIN_SPEED = 10


global sendBack_angle, sendBack_Speed, current_speed, current_angle
sendBack_angle = 0
sendBack_Speed = 0
current_speed = 0
current_angle = 0


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


PORT = 54321

net.load_model(49,"0.2270")
s.connect(('host.docker.internal', PORT))


def Control(angle, speed):
    global sendBack_angle, sendBack_Speed
    sendBack_angle = angle
    sendBack_Speed = speed


if __name__ == "__main__":
    print('Wait a minute')

    try:
        while True:
            message = bytes(f"1 {sendBack_angle} {sendBack_Speed}", "utf-8")
            s.sendall(message)
            data = s.recv(100000)

            try:
                image = cv2.imdecode(
                    np.frombuffer(
                        data,
                        np.uint8
                        ), -1
                    )


                #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image = cv2.resize(image,(512,256))


                x, y = net.predict(image)
                fits = np.array([np.polyfit(_y, _x, 1) if len(_x) < 5  else  np.polyfit(_y, _x, 2) for _x, _y in zip(x, y)])
                fits = np.array([np.polyfit(_y, _x, 1) for _x, _y in zip(x, y)])
                
                fits = util.adjust_fits(fits)

                sendBack_angle = util.get_steer_angle(fits, current_speed)


                if sendBack_Speed > MAX_SPEED:
                    sendBack_Speed = 5
                if sendBack_Speed < 10:
                    sendBack_Speed = 35

                cv2.waitKey(1)


            except Exception as er:
                pass

    finally:
        print('closing socket')
        s.close()
