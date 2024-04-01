import os
from detection import color_Detection
from peripheral import Camera
from tools import load_json

os.system('pyclean .')
os.system('cls')

PATH_CONFIG_DETECTION = 'config\config_detection_red_color.json'
config_detection = load_json(PATH_CONFIG_DETECTION)
red = color_Detection(**config_detection)
cam = Camera(0)

no_exit = True
while no_exit:
  frame = cam.get_frame()
  windows = red.detection_one(frame)
  if not(windows is None):
    frame = cam.draw_rec(frame, windows, color=(255, 0, 0))
    frame = cam.write_text(frame, text=f'{cam.point_center - windows.point_center}', org=(100, 100))
  no_exit = not(cam.live_view(frame))
  