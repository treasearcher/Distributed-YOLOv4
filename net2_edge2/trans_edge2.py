import threading
import queue
from socket import *
import numpy as np
import _thread
import cv2
import time


qsize = 5


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


class trans_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.inQue = queue.Queue(qsize)
        self.outQue = queue.Queue(qsize)
        self.img = queue.Queue(qsize)
        self.lock = threading.Lock()
        self.c_cam = socket(AF_INET, SOCK_STREAM)
        self.c_cam.connect(('localhost', 25000))
        self.c_n1 = socket(AF_INET, SOCK_STREAM)
        self.c_n1.connect(('localhost', 25001))
        self.fps = 0
        self.fps_dis = 0

    def fillData(self,data):
        if not self.outQue.full():
            self.lock.acquire()
            self.outQue.put(data)
            self.lock.release()

    def fps_update(self):
        while 1:
            time.sleep(1)
            self.fps_dis = self.fps
            self.fps=0

    def recv_img(self):
        arr = np.zeros(shape=(480, 640, 3), dtype=np.uint8)
        while 1:
            if not self.img.full():
                recv_into(arr, self.c_cam)
                self.lock.acquire()
                self.img.put(arr)
                self.lock.release()
            else:
                time.sleep(0.01)

    def recv_mid(self):
        y11 = np.zeros(shape=(1,17328,1,4), dtype=np.float32)
        y12 = np.zeros(shape=(1,17328,80), dtype=np.float32)
        x10=np.zeros(shape=(1,255,38,38), dtype=np.float32)
        x18=np.zeros(shape=(1, 255, 19, 19), dtype=np.float32)
        while 1:
            if not self.outQue.full():
                recv_into(y11, self.c_n1)
                recv_into(y12, self.c_n1)
                recv_into(x10, self.c_n1)
                recv_into(x18, self.c_n1)
                self.lock.acquire()
                self.inQue.put((y11,y12,x10,x18))
                self.lock.release()
            else:
                time.sleep(0.01)

    def display(self):
        while 1:
            if not self.outQue.empty() and not self.img.empty():
                self.fps += 1
                self.lock.acquire()
                img = self.outQue.get()
                self.lock.release()
                img = cv2.putText(img, 'FPS: {}'.format(self.fps_dis), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2)
                cv2.imshow('fps', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                time.sleep(0.01)

    def run(self):
        _thread.start_new_thread(self.fps_update, ())
        _thread.start_new_thread(self.recv_img, ())
        _thread.start_new_thread(self.recv_mid, ())
        _thread.start_new_thread(self.display, ())
