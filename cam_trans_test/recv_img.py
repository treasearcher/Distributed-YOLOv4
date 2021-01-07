import cv2
import json
from socket import *
# import socket
import numpy as np
import time

def send_from(arr, dest):
    view = memoryview(arr).cast('B')
    while len(view):
        nsent = dest.send(view)
        view = view[nsent:]

def recv_into(arr, source):
    view = memoryview(arr).cast('B')
    while len(view):
        nrecv = source.recv_into(view)
        view = view[nrecv:]

c = socket(AF_INET, SOCK_STREAM)
c.connect(('localhost', 25000))
img = np.zeros(shape=(480, 640, 3), dtype=np.uint8)
while(1):
    recv_into(img, c)  ######################################################################
    # print(img)
    cv2.imshow('111', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

c.close()
