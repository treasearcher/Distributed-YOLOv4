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
update = False
def time_check():
    while 1:
        global update
        update=True
        time.sleep(1)
        update=False
        # print(1)
# def key_check(c):
#     global FLAG
#     while FLAG:
#         key=readkey()
#         if key == 'q':
#             global FLAG
#             FLAG=False
#             c.close()
#         global update
#         update = True
#         time.sleep(1)
#         update = False


import cv2
import _thread
if __name__ == "__main__":

    namesfile = 'data/coco.names'
    c = socket(AF_INET, SOCK_STREAM)
    c.connect(('localhost', 25002))

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
        # print(img)
        if update:
            tmp_fps = fps
            fps = 0
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
