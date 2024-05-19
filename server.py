import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
import glfw
import ctypes
import win32api
from OpenGL.GL import *
import imgui
from imgui.integrations.glfw import GlfwRenderer
import io

POS = []
fov = 420

imgui.create_context()
glfw.init()
glfw.window_hint(glfw.FLOATING, True)
glfw.window_hint(glfw.RESIZABLE, False)
glfw.window_hint(glfw.DECORATED, False)
glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, True)

window = glfw.create_window(1920, 1079, "hyzr", None, None)
if not window:
    glfw.terminate()

# Import ctypes library for calling Windows API functions
from ctypes import wintypes

# Define constants for SetWindowDisplayAffinity
WDA_NONE = 0x00000000
WDA_MONITOR = 0x00000001
WDA_EXCLUDEFROMCAPTURE = 0x00000011

# Load the user32 DLL
user32 = ctypes.WinDLL('user32', use_last_error=True)

# Define the SetWindowDisplayAffinity function prototype
user32.SetWindowDisplayAffinity.restype = wintypes.BOOL
user32.SetWindowDisplayAffinity.argtypes = [wintypes.HWND, wintypes.DWORD]

def set_window_display_affinity(hwnd, affinity):
    result = user32.SetWindowDisplayAffinity(hwnd, affinity)
    if not result:
        raise ctypes.WinError(ctypes.get_last_error())
    return result


glfw.make_context_current(window)
glfw.swap_interval(0)

hwnd = glfw.get_win32_window(window)
exstyle = ctypes.windll.user32.GetWindowLongW(hwnd, -20)  # GWL_EXSTYLE
exstyle |= 0x80000  # WS_EX_LAYERED
exstyle |= 0x20  # WS_EX_TRANSPARENT
ctypes.windll.user32.SetWindowLongW(
    hwnd, -20, exstyle
)  # Set extended style
ctypes.windll.user32.SetLayeredWindowAttributes(
    hwnd, 0, 255, 2
)  # Set transparency
glViewport(0, 0, 1920, 1079)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(0, 1920, 1079, 0, 1, -1)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
impl = GlfwRenderer(window)
imgui.get_io().ini_file_name = "".encode()
imgui.create_context()
imgui_io = imgui.get_io()
imgui_renderer = GlfwRenderer(window)
io = imgui.get_io()

set_window_display_affinity(hwnd, WDA_EXCLUDEFROMCAPTURE)

import zmq
italic = io.fonts.add_font_from_file_ttf(
    "C:/Windows/Fonts/SEGUIBLI.TTF",
    20,
)
bold = io.fonts.add_font_from_file_ttf(
    "C:/Windows/Fonts/verdanab.ttf",
    12,
)

# bold = io.fonts.add_font_from_file_ttf(
#     "C:/Users/hyper/Downloads/fuzr/Fortnite.TTF",
#     15,
# )

# SKELE = imgui.get_color_u32_rgba(1, 0.2, 0, 1)
# WHITE = imgui.get_color_u32_rgba(1, 1, 1, 1)
# BOX = imgui.get_color_u32_rgba(1, 0, 0, 1)

SKELE = imgui.get_color_u32_rgba(0, 1, 0, 1)
SKELE2 = imgui.get_color_u32_rgba(1, 0, 0, 1)
WHITE = imgui.get_color_u32_rgba(1, 0.9, 0, 1)
BOX = imgui.get_color_u32_rgba(1, 0, 0, 1)
BOX2 = imgui.get_color_u32_rgba(1, 0, 1, 1)

FOV = imgui.get_color_u32_rgba(0, 0, 0, 1)
# WHITE = imgui.get_color_u32_rgba(1, 135/255, 110/255, 1)
SKELE_THICKNESS = 2
impl.refresh_font_texture()

context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.bind("tcp://*:12345")

def start():
    global POS, bold
    while not glfw.window_should_close(window):
        glfw.poll_events()
        imgui.new_frame() 
        impl.process_inputs()
        dl = imgui.get_background_draw_list()
        try:
            message = socket.recv()
            data = message.decode('utf-8').strip().split(" ")
            if len(data) == 0: POS = []
            coordinates = [(int(float(data[i])), int(float(data[i+1]))) for i in range(0, len(data), 2)]
            POS = [coordinates[i:i+18] for i in range(0, len(coordinates), 18)]
        except: POS = []

        fps = int(imgui.get_io().framerate)
        fps_text = f"FPS: {fps}"
        text_size = imgui.calc_text_size(fps_text)
        dl.add_text(10, 10, imgui.get_color_u32_rgba(1, 1, 1, 1), fps_text)

        for player in POS:
            if player[15][1] == 1:
                if win32api.GetAsyncKeyState(0X02) == 0:
                    dl.add_line(player[0][0], (player[0][1]), player[2][0], player[2][1], SKELE, SKELE_THICKNESS)
                    dl.add_line(player[1][0], player[1][1], player[2][0], player[2][1], SKELE, SKELE_THICKNESS)
                    dl.add_line(player[3][0], player[3][1], player[2][0], player[2][1], SKELE, SKELE_THICKNESS)
                    dl.add_line(player[4][0], player[4][1], player[2][0], player[2][1], SKELE, SKELE_THICKNESS)
                    dl.add_line(player[5][0], player[5][1], player[3][0], player[3][1], SKELE, SKELE_THICKNESS)
                    dl.add_line(player[6][0], player[6][1], player[4][0], player[4][1], SKELE, SKELE_THICKNESS)
                    dl.add_line(player[5][0], player[5][1], player[7][0], player[7][1], SKELE, SKELE_THICKNESS)
                    dl.add_line(player[6][0], player[6][1], player[8][0], player[8][1], SKELE, SKELE_THICKNESS)
                    dl.add_line(player[10][0], player[10][1], player[1][0], player[1][1], SKELE, SKELE_THICKNESS)
                    dl.add_line(player[9][0], player[9][1], player[1][0], player[1][1], SKELE, SKELE_THICKNESS)
                    dl.add_line(player[12][0], player[12][1], player[10][0], player[10][1], SKELE, SKELE_THICKNESS)
                    dl.add_line(player[11][0], player[11][1], player[9][0], player[9][1], SKELE, SKELE_THICKNESS)
                    dl.add_line(player[13][0], player[13][1], player[12][0], player[12][1], SKELE, SKELE_THICKNESS)
                    dl.add_line(player[14][0], player[14][1], player[11][0], player[11][1], SKELE, SKELE_THICKNESS)
            if player[15][1] == 0:
                if win32api.GetAsyncKeyState(0X02) == 0:
                    dl.add_line(player[0][0], (player[0][1]), player[2][0], player[2][1], SKELE2, SKELE_THICKNESS)
                    dl.add_line(player[1][0], player[1][1], player[2][0], player[2][1], SKELE2, SKELE_THICKNESS)
                    dl.add_line(player[3][0], player[3][1], player[2][0], player[2][1], SKELE2, SKELE_THICKNESS)
                    dl.add_line(player[4][0], player[4][1], player[2][0], player[2][1], SKELE2, SKELE_THICKNESS)
                    dl.add_line(player[5][0], player[5][1], player[3][0], player[3][1], SKELE2, SKELE_THICKNESS)
                    dl.add_line(player[6][0], player[6][1], player[4][0], player[4][1], SKELE2, SKELE_THICKNESS)
                    dl.add_line(player[5][0], player[5][1], player[7][0], player[7][1], SKELE2, SKELE_THICKNESS)
                    dl.add_line(player[6][0], player[6][1], player[8][0], player[8][1], SKELE2, SKELE_THICKNESS)
                    dl.add_line(player[10][0], player[10][1], player[1][0], player[1][1], SKELE2, SKELE_THICKNESS)
                    dl.add_line(player[9][0], player[9][1], player[1][0], player[1][1], SKELE2, SKELE_THICKNESS)
                    dl.add_line(player[12][0], player[12][1], player[10][0], player[10][1], SKELE2, SKELE_THICKNESS)
                    dl.add_line(player[11][0], player[11][1], player[9][0], player[9][1], SKELE2, SKELE_THICKNESS)
                    dl.add_line(player[13][0], player[13][1], player[12][0], player[12][1], SKELE2, SKELE_THICKNESS)
                    dl.add_line(player[14][0], player[14][1], player[11][0], player[11][1], SKELE2, SKELE_THICKNESS)

            distanceStr = "(" + str(player[15][0]) + "m)"
            cornerHeight = float(player[16][0])
            cornerWidth = float(player[16][1])
            headboxX = float(player[17][0])
            headboxY = float(player[17][1])
            with imgui.font(bold):  
                text_size = imgui.calc_text_size(distanceStr)
                outline_color = imgui.get_color_u32_rgba(0, 0, 0, 1)
                outline_thickness = 2
                # for i in range(-outline_thickness, outline_thickness):
                #     for j in range(-outline_thickness, outline_thickness + 2):
                #         if i != 0 or j != 0:
                #             dl.add_text(headboxX - text_size[0]/2 + i, headboxY + cornerHeight + j - text_size[1]/2, outline_color, distanceStr)

                # dl.add_circle(headboxX, (player[0][1]), cornerWidth/15, SKELE, 100, SKELE_THICKNESS)
                dl.add_text(headboxX - text_size[0]/2, headboxY - text_size[1]/2, WHITE, distanceStr)
            # if player[15][1] == 0:

            #     # dl.add_rect(headboxX - (cornerWidth/2) - 2, headboxY - 2, headboxX - (cornerWidth/2) + cornerWidth + 2, headboxY + cornerHeight + 2, BOX, 2, 2, 2)
            #     dl.add_line(headboxX - (cornerWidth/2) - 2, headboxY - 2, headboxX - (cornerWidth/2) - 2 + cornerWidth/6, headboxY - 2, BOX, 2)
            #     dl.add_line(headboxX - (cornerWidth/2) - 2, headboxY - 2, headboxX - (cornerWidth/2) - 2, headboxY - 2 + cornerWidth/6, BOX, 2)

            #     # dl.add_line(headboxX - (cornerWidth/2) + cornerWidth + 2, headboxY + cornerHeight + 2, headboxX - (cornerWidth/2) - 2 - cornerWidth/10, headboxY - 2, BOX, 2)
            #     dl.add_line(headboxX - (cornerWidth/2) + cornerWidth + 2, headboxY - 2, headboxX - (cornerWidth/2) + cornerWidth + 2 - cornerWidth/6, headboxY - 2, BOX, 2)
            #     dl.add_line(headboxX - (cornerWidth/2) + cornerWidth + 2, headboxY - 2, headboxX - (cornerWidth/2) + cornerWidth + 2, headboxY - 2 + cornerWidth/6, BOX, 2)

            #     dl.add_line(headboxX - (cornerWidth/2) + cornerWidth + 2, headboxY + cornerHeight + 2, headboxX - (cornerWidth/2) + cornerWidth + 2 - cornerWidth/6, headboxY + cornerHeight + 2, BOX, 2)
            #     dl.add_line(headboxX - (cornerWidth/2) + cornerWidth + 2, headboxY + cornerHeight + 2, headboxX - (cornerWidth/2) + cornerWidth + 2, headboxY + cornerHeight + 2 - cornerWidth/6, BOX, 2)

            #     dl.add_line(headboxX - (cornerWidth/2) - 2, headboxY + cornerHeight + 2, headboxX - (cornerWidth/2) - 2 + cornerWidth/6, headboxY + cornerHeight + 2, BOX, 2)
            #     dl.add_line(headboxX - (cornerWidth/2) - 2, headboxY + cornerHeight + 2, headboxX - (cornerWidth/2) - 2, headboxY + cornerHeight + 2 - cornerWidth/6, BOX, 2)
            
            # if player[15][1] == 1:
            #     dl.add_line(headboxX - (cornerWidth/2) - 2, headboxY - 2, headboxX - (cornerWidth/2) - 2 + cornerWidth/6, headboxY - 2, BOX2, 2)
            #     dl.add_line(headboxX - (cornerWidth/2) - 2, headboxY - 2, headboxX - (cornerWidth/2) - 2, headboxY - 2 + cornerWidth/6, BOX2, 2)

            #     # dl.add_line(headboxX - (cornerWidth/2) + cornerWidth + 2, headboxY + cornerHeight + 2, headboxX - (cornerWidth/2) - 2 - cornerWidth/10, headboxY - 2, BOX, 2)
            #     dl.add_line(headboxX - (cornerWidth/2) + cornerWidth + 2, headboxY - 2, headboxX - (cornerWidth/2) + cornerWidth + 2 - cornerWidth/6, headboxY - 2, BOX2, 2)
            #     dl.add_line(headboxX - (cornerWidth/2) + cornerWidth + 2, headboxY - 2, headboxX - (cornerWidth/2) + cornerWidth + 2, headboxY - 2 + cornerWidth/6, BOX2, 2)

            #     dl.add_line(headboxX - (cornerWidth/2) + cornerWidth + 2, headboxY + cornerHeight + 2, headboxX - (cornerWidth/2) + cornerWidth + 2 - cornerWidth/6, headboxY + cornerHeight + 2, BOX2, 2)
            #     dl.add_line(headboxX - (cornerWidth/2) + cornerWidth + 2, headboxY + cornerHeight + 2, headboxX - (cornerWidth/2) + cornerWidth + 2, headboxY + cornerHeight + 2 - cornerWidth/6, BOX2, 2)

            #     dl.add_line(headboxX - (cornerWidth/2) - 2, headboxY + cornerHeight + 2, headboxX - (cornerWidth/2) - 2 + cornerWidth/6, headboxY + cornerHeight + 2, BOX2, 2)
            #     dl.add_line(headboxX - (cornerWidth/2) - 2, headboxY + cornerHeight + 2, headboxX - (cornerWidth/2) - 2, headboxY + cornerHeight + 2 - cornerWidth/6, BOX2, 2)
        dl.add_circle(1920/2, 1080/2, 75, FOV, 200, 2)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        imgui.render()
        imgui_renderer.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

if __name__ == "__main__":
    start()
