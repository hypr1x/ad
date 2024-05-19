import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
import glfw
import ctypes
import win32api
from OpenGL.GL import *
from math import * 
import zmq

POS = []
fov = 420

glfw.init()
glfw.window_hint(glfw.FLOATING, True)
glfw.window_hint(glfw.RESIZABLE, False)
glfw.window_hint(glfw.DECORATED, False)
glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, True)
glfw.window_hint(glfw.SAMPLES, 4)  # Enable multisampling

window = glfw.create_window(1920, 1079, "hyzr", None, None)
if not window:
    glfw.terminate()

glfw.make_context_current(window)
glfw.swap_interval(0)

hwnd = glfw.get_win32_window(window)
exstyle = ctypes.windll.user32.GetWindowLongW(hwnd, -20)  # GWL_EXSTYLE
exstyle |= 0x80000  # WS_EX_LAYERED
exstyle |= 0x20  # WS_EX_TRANSPARENT
ctypes.windll.user32.SetWindowLongW(hwnd, -20, exstyle)  # Set extended style
ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, 255, 2)  # Set transparency
glViewport(0, 0, 1920, 1079)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(0, 1920, 1079, 0, 1, -1)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glEnable(GL_MULTISAMPLE)  # Enable multisampling

context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.bind("tcp://*:12345")

def start():
    global POS
    while not glfw.window_should_close(window):
        glfw.poll_events()
        try:
            message = socket.recv()
            data = message.decode('utf-8').strip().split(" ")
            if len(data) == 0: POS = []
            coordinates = [(int(float(data[i])), int(float(data[i+1]))) for i in range(0, len(data), 2)]
            POS = [coordinates[i:i+18] for i in range(0, len(coordinates), 18)]
        except: POS = []

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_LINE_SMOOTH)  # Enable line smoothing
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)  # Set line smoothing hint to the highest quality
        glLineWidth(2.0)  # Set line width
        glBegin(GL_LINES)
        for player in POS:
            glColor3f(1, 0, 0)  # Red color for skeleton
            glVertex2f(player[0][0], player[0][1])
            glVertex2f(player[2][0], player[2][1])

            glVertex2f(player[1][0], player[1][1])
            glVertex2f(player[2][0], player[2][1])

            glVertex2f(player[3][0], player[3][1])
            glVertex2f(player[2][0], player[2][1])

            glVertex2f(player[4][0], player[4][1])
            glVertex2f(player[2][0], player[2][1])

            glVertex2f(player[5][0], player[5][1])
            glVertex2f(player[3][0], player[3][1])

            glVertex2f(player[6][0], player[6][1])
            glVertex2f(player[4][0], player[4][1])

            glVertex2f(player[5][0], player[5][1])
            glVertex2f(player[7][0], player[7][1])

            glVertex2f(player[6][0], player[6][1])
            glVertex2f(player[8][0], player[8][1])

            glVertex2f(player[10][0], player[10][1])
            glVertex2f(player[1][0], player[1][1])

            glVertex2f(player[9][0], player[9][1])
            glVertex2f(player[1][0], player[1][1])

            glVertex2f(player[12][0], player[12][1])
            glVertex2f(player[10][0], player[10][1])

            glVertex2f(player[11][0], player[11][1])
            glVertex2f(player[9][0], player[9][1])

            glVertex2f(player[13][0], player[13][1])
            glVertex2f(player[12][0], player[12][1])

            glVertex2f(player[14][0], player[14][1])
            glVertex2f(player[11][0], player[11][1])
        glEnd()

        # Render FOV circle
        glColor4f(0, 0, 0, 1)
        glBegin(GL_LINE_LOOP)
        for i in range(200):
            theta = 2.0 * 3.1415926 * i / 200
            x = 1920/2 + 75 * cos(theta)
            y = 1080/2 + 75 * sin(theta)
            glVertex2f(x, y)
        glEnd()

        glfw.swap_buffers(window)

if __name__ == "__main__":
    start()
