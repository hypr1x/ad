import numpy as np
import torch
import math
import bettercam
import win32api
fov = 350
model = torch.hub.load('ultralytics/yolov5', "custom", path="best.pt", verbose=False)
camera = bettercam.create()
while True:
    left, top = (1920 - fov) // 2, (1080 - fov) // 2
    region = (left, top, left + fov, top + fov)
    frame = camera.grab(region=region)
    if not frame is None:
        results = model(np.array(frame))
        if len(results.xyxy[0]) == 0: continue
        least_crosshair_dist = closest_detection = False
        for *box, conf, _ in results.xyxy[0]: 
            x1y1, x2y2 = [int(x.item()) for x in box[:2]], [int(x.item()) for x in box[2:]]
            x1, y1, x2, y2, conf = *x1y1, *x2y2, conf.item()
            relative_head_X, relative_head_Y, own_player = int((x1 + x2) / 2), int((y1 + y2) / 2 - (y2 - y1) / 2.51), x1 < 15 or (x1 < fov / 5 and y2 > fov / 1.2)
            crosshair_dist = math.dist((relative_head_X, relative_head_Y),(fov / 2, fov / 2)) 
            if not least_crosshair_dist: least_crosshair_dist = crosshair_dist 
            if crosshair_dist <= least_crosshair_dist and not own_player: least_crosshair_dist, closest_detection = crosshair_dist, {"x1y1": x1y1, "x2y2": x2y2, "relative_head_X": relative_head_X, "relative_head_Y": relative_head_Y, "conf": conf }
            if own_player: own_player = False 
        if closest_detection: 
            # for i in range(0, 10): 
            win32api.mouse_event(1, int((closest_detection["relative_head_X"]-fov/2)/2), int((closest_detection["relative_head_Y"]-fov/2)/2), 0, 0)
