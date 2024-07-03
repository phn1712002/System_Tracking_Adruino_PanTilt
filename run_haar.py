import os
from mechanicalStructure import pan_Tilt_Haar
from tools import load_json

#! Clean pycached
os.system('pyclean .')
os.system('cls')

#! Run
path_config_pan_tilt = './config/config_pantilt.json'
path_config_detection = './config/config_detection_haar.json'
path_config_xml = './.model/haarcascades/haarcascade_frontalface_default.xml'
pan_titl = pan_Tilt_Haar(path_config_xml=path_config_xml, 
                         config_detection=load_json(path_config_detection), 
                         config_pantilt=load_json(path_config_pan_tilt))
pan_titl.status_launch()
pan_titl.tracking_face()

