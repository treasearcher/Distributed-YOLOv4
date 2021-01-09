from tool.torch_utils import *
from tool.utils import load_class_names, plot_boxes_cv2
from socket import *
# import sys
# import tty
# import termios
# import _thread
# import time
#
#
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
#
#
#
# def readchar():
#     fd = sys.stdin.fileno()
#     old_settings = termios.tcgetattr(fd)
#     try:
#         tty.setraw(sys.stdin.fileno())
#         ch = sys.stdin.read(1)
#     finally:
#         termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#     return ch
#
#
# def readkey(getchar_fn=None):
#     getchar = getchar_fn or readchar
#     c1 = getchar()
#     if ord(c1) != 0x1b:
#         return c1
#     c2 = getchar()
#     if ord(c2) != 0x5b:
#         return c1
#     c3 = getchar()
#     return chr(0x10 + ord(c3) - 65)

FLAG = True
fps = 0
tmp_fps = 0
def time_check():
    global fps, tmp_fps
    while 1:
        time.sleep(1)
        tmp_fps=fps
        fps=0


import cv2
import _thread
if __name__ == "__main__":

    namesfile = 'data/coco.names'
    c = socket(AF_INET, SOCK_STREAM)
    c.connect(('192.168.1.103', 25002))

    class_names = load_class_names(namesfile)
    _thread.start_new_thread(time_check, ())
    fps=0
    tmp_fps = 0
    img = np.zeros(shape=(480, 640, 3), dtype=np.uint8)
    while FLAG:
        recv_into(img,c)
        # boxes=np.zeros(shape=(1,3,7), dtype=np.float32)
        # recv_into(boxes,c)
        fps+=1
        # frame=plot_boxes_cv2(img, boxes[0], tmp_fps, class_names)
        img = cv2.putText(img, 'FPS: {}'.format(tmp_fps), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2)
        cv2.imshow("capture", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
