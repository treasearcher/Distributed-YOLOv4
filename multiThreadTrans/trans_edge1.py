import threading
import queue
from socket import *
import numpy as np
import _thread


qsize=5


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
        self.lock = threading.Lock
        self.inQue = queue.Queue(qsize)
        self.outQue = queue.Queue(qsize)
        self.client = socket(AF_INET, SOCK_STREAM)
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind(('', 25001))
        self.server.listen(1)
        self.a_clinet = self.server.accept()
        self.client.connect(('localhost', 25000))

    def fillData(self, data):
        if not self.outQue.full():
            self.lock.acquire()
            self.outQue.put(data)
            self.lock.release()

    def recv(self):
        arr = np.zeros(shape=(480, 640, 3), dtype=np.uint8)
        while 1:
            if not self.inQue.full():
                recv_into(arr, self.client)
                self.lock.acquire()
                self.inQue.put(arr)
                self.lock.release()

    def send(self):
        while 1:
            if not self.outQue.empty():
                self.lock.acquire()
                out_tuple=self.outQue.get()
                self.lock.release()
                for i in range(out_tuple):
                    send_from(out_tuple[i], self.a_clinet)

    def run(self):
        _thread.start_new_thread(self.recv, ())
        _thread.start_new_thread(self.send, ())

# def print_time(threadName, delay, counter):
#     while counter:
#         if exitFlag:
#             threadName.exit()
#         time.sleep(delay)
#         print ("%s: %s" % (threadName, time.ctime(time.time())))
#         counter -= 1
