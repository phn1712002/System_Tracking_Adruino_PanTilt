import os
from detection import face_Detection_Haar
from peripheral import Camera
from tools import load_json

os.system('pyclean .')
os.system('cls')

PATH_CONFIG_DETECTION = 'config\config_detection_haar.json'
PATH_XML_HAAR = 'config\haarcascade_frontalface_default.xml'

face = face_Detection_Haar(path_config_xml=PATH_XML_HAAR, config_detection=load_json(PATH_CONFIG_DETECTION))
cam = Camera(0)

no_exit = True
while no_exit:
  frame = cam.get_frame()
  windows = face.detection_one_face(frame)
  if not(windows is None):
    frame = cam.draw_rec(frame, windows, color=(255, 0, 0))
    frame = cam.write_text(frame, text=f'{cam.point_center - windows.point_center}', org=(100, 100))
  no_exit = not(cam.live_view(frame))
  