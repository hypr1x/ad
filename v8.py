from ultralytics import YOLO
import torch
import numpy as np
import math
import bettercam
import win32api
import glfw
import ctypes
from OpenGL.GL import *
import imgui
from imgui.integrations.glfw import GlfwRenderer
import base64
import io
import OpenGL.GL as gl

camera = bettercam.create()
model = YOLO('yolov8n.pt', task='detect', verbose=True)

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

glfw.make_context_current(window)
glfw.swap_interval(0)

# Set window attributes for transparency (Windows-specific)
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
# while True:pass
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
impl.refresh_font_texture()
mainColor = (0.376, 0.698, 0.988, 1.0)

def calc_movement(target_x, target_y):
    offset_x = target_x - 1920/2
    offset_y = target_y - 1080/2

    degrees_per_pixel_x = fov / 1920
    degrees_per_pixel_y = fov / 1080
    
    mouse_move_x = offset_x * degrees_per_pixel_x

    move_x = (mouse_move_x / 360) * (800 * (1 / 1))

    mouse_move_y = offset_y * degrees_per_pixel_y
    move_y = (mouse_move_y / 360) * (800 * (1 / 1))
    return move_x, move_y

while not glfw.window_should_close(window):


    glfw.poll_events()
    imgui.new_frame() 
    impl.process_inputs()
    left, top = (1920 - fov) // 2, (1080 - fov) // 2
    region = (left, top, left + fov, top + fov)
    frame = camera.grab(region=region)
    # if npImg.shape[3] == 4:
    #     # If the image has an alpha channel, remove it
    #     npImg = npImg[:, :, :, :3]

    # if True: # JinxTheCatto
    #     if False:
    #         npImg[:, -maskHeight:, (screenShotWidth - maskWidth):, :] = 0
    #     elif True == "Left":
    #         npImg[:, -200:, :200, :] = 0

    # im = npImg / 255
    # im = im.astype(np.half)

    # im = np.moveaxis(im, 3, 1)
    # im = torch.from_numpy(np.asnumpy(im)).to('cuda')


    if not frame is None:
        # results = model(np.array(frame), verbose=False)
        results = model(
        np.array(frame),        
        # iou=0.3,
        # conf=0.4,
        verbose=False,
        )
        # print(results)
        for frame in results:
            boxes_array = frame.boxes.xywh.to("cuda:0")
            if len(boxes_array) > 0:
                numbers = [value.item() for value in boxes_array[0]]   
                x1 = numbers[0] - numbers[2]/2
                y1 = numbers[1] - numbers[3]/2
                x2 = numbers[1] + numbers[2]/2
                y2 = numbers[1] + numbers[3]/2

                imgui.get_background_draw_list().add_rect(numbers[0] + left - numbers[2]/2, numbers[1] + top - numbers[3]/2, numbers[0] + left + numbers[2]/2, numbers[1] + top + numbers[3]/2, imgui.get_color_u32_rgba(1, 0, 0, 1))
                relative_head_X, relative_head_Y, own_player = int((x1 + x2) / 2), int((y1 + y2) / 2 - (y2 - y1) / 2.51), x1 < 15 or (x1 < fov / 5 and y2 > fov / 1.2)

                if not own_player:
                    win32api.mouse_event(1, int((relative_head_X-fov/2)/2), int((relative_head_Y-fov/2)/2), 0, 0)
                


    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    imgui.render()
    imgui_renderer.render(imgui.get_draw_data())
    glfw.swap_buffers(window)

