import os
from mechanicalStructure import pan_Tilt_Red_Color
from tools import load_json

#! Clean pycached
os.system('pyclean .')
os.system('cls')

#! Run
path_config_pan_tilt = './config/config_pantilt.json'
path_config_detection = './config/config_detection_red_color.json'
pan_titl = pan_Tilt_Red_Color(config_detection=load_json(path_config_detection), 
                              config_pantilt=load_json(path_config_pan_tilt))
pan_titl.status_launch()
pan_titl.tracking_face()

