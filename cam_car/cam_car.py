import cv2
import json
from socket import *
# import socket

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


s = socket(AF_INET, SOCK_STREAM)
s.bind(('', 25000))
s.listen(2)
c,a = s.accept()
c_2,a_2=s.accept()
c_3,a_3=s.accept()
cap = cv2.VideoCapture(0)
flag = cap.isOpened()
print(flag)
while (1):
    # get a frame
    _, frame = cap.read()
    # show a frame
    send_from(frame, c)
    send_from(frame, c_2)
    # send_from(frame, c_3)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
c.close()
c_2.close()
s.close()