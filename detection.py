import cv2, numpy as np
from typing import Any, Dict
from geo import Point, Rectangle
   
class face_Detection_Haar:
  def __init__(self, path_config_xml:str='', config_detection:Dict={}) -> None:
    self.path_config_xml = path_config_xml
    self.config_detection = config_detection
    self.detectors = cv2.CascadeClassifier(self.path_config_xml)
    
    
  def detection(self, frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faceRects = self.detectors.detectMultiScale(gray, **self.config_detection, flags=cv2.CASCADE_SCALE_IMAGE)
    
    face_ROI = []
    for (fX, fY, fW, fH) in faceRects:
      rec = Rectangle([Point(x=fX, y=fY), 
                       Point(x=fX + fW, y=fY + fH), 
                       Point(x=fX, y=fY + fH), 
                       Point(x=fX + fW, y=fY)
                       ])
      face_ROI.append(rec)
    return face_ROI
  
  def detection_one_face(self, frame):
    face = None
    face_ROI = self.detection(frame)
    if len(face_ROI) != 0:
      idx_max = np.argmax([rec.area for rec in face_ROI])
      face = face_ROI[idx_max]
    return face
  
class color_Detection:
  def __init__(self, low_RGB=[161, 155, 84], high_RGB=[179, 255, 255], reverse=True) -> None:
    self.low_RGB = np.array(low_RGB)
    self.high_RGB = np.array(high_RGB)
    self.reverse = reverse

  def detection(self, frame):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_frame, self.low_RGB, self.high_RGB)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=self.reverse)

    red_ROI = []
    for cnt in contours:
        (fX, fY, fW, fH) = cv2.boundingRect(cnt)
        rec = Rectangle([Point(x=fX, y=fY), 
                       Point(x=fX + fW, y=fY + fH), 
                       Point(x=fX, y=fY + fH), 
                       Point(x=fX + fW, y=fY)
                       ])
        red_ROI.append(rec)
    return red_ROI
  
  def detection_one(self, frame):
    red_rec = None
    red_ROI = self.detection(frame)
    if len(red_ROI) != 0:
      idx_max = np.argmax([rec.area for rec in red_ROI])
      red_rec = red_ROI[idx_max]
    return red_rec