import pyfirmata, threading
from typing import Any, Dict
from motor import model_RC_Servo_MG995
from peripheral import Camera
from optimization import optimization_Control_2Motor
from tools import delay_microseconds
from detection import face_Detection_Haar, color_Detection
from motor import Motor
from switch import Switch

#! Pan tilt
class pan_Tilt:
    def __init__(self, config_pantilt: Dict = {}) -> None:

        self.config_pantilt = config_pantilt
        self.config_adruino = config_pantilt["ADRUINO"]
        self.config_camera = config_pantilt["CAMERA"]
        self.config_optimization = config_pantilt["OPTI"]
        self.delay_ms = config_pantilt["delay_ms"]

        self.board = pyfirmata.Arduino(self.config_adruino["COM"])
        pyfirmata.util.Iterator(self.board).start()

        self.optimization = optimization_Control_2Motor(**self.config_optimization)

        self.motor_link_1 = model_RC_Servo_MG995(
            self.board, **self.config_adruino["LINK_1"]
        )
        self.motor_link_2 = model_RC_Servo_MG995(
            self.board, **self.config_adruino["LINK_2"]
        )
        self.cam = Camera(**self.config_camera)

        self.func_delay = delay_microseconds
        self.exit = None

        self.face_detection = lambda frame: None
        self.frame_current = None
        self.er_current = None

    def status_launch(self, angle_launch_motor_1=85, angle_launch_motor_2=45):
        no_exit = True
        while no_exit:
            no_exit = False
            if self.motor_link_1.angle_current < angle_launch_motor_1:
                self.motor_link_1.step()
                no_exit = True
            if self.motor_link_2.angle_current < angle_launch_motor_2:
                self.motor_link_2.step()
                no_exit = True
            self.func_delay(self.delay_ms)

    def control_pan_tilt(self):
        while not (self.exit):
            if not (self.frame_current is None):
                face = self.face_detection(self.frame_current)
                if not (face is None):
                    self.er_current = self.cam.point_center - face.point_center
                    step_x, step_y = self.optimization.calc_amount_correnction(
                        self.er_current.x, self.er_current.y
                    )
                    self.motor_link_1.step(step_x)
                    self.motor_link_2.step(step_y)
                    self.func_delay(self.delay_ms)
                else:
                    self.er_current = None

    def tracking_face(self):
        self.exit = False
        threading_control_pan_tilt = threading.Thread(target=self.control_pan_tilt)
        threading_control_pan_tilt.start()
        while not (self.exit):
            self.frame_current = self.cam.get_frame()
            if not (self.er_current is None):
                frame_draw = self.cam.write_text(
                    self.frame_current, text=f"Error: {self.er_current}", org=(100, 100)
                )
                frame_draw = self.cam.draw_circle_with_point(
                    frame=frame_draw, point=self.cam.point_center, color=(0, 255, 0)
                )
                if not (self.er_current is None):
                    frame_draw = self.cam.draw_circle_with_point(
                        frame=frame_draw,
                        point=(self.cam.point_center - self.er_current),
                        color=(0, 0, 255),
                    )
                self.exit = self.cam.live_view(frame_draw)
            else:
                self.exit = self.cam.live_view(self.frame_current)
        threading_control_pan_tilt.join()

class pan_Tilt_Haar(pan_Tilt):
    def __init__(
        self,
        path_config_xml: str = "./.model/haarcascades/haarcascade_frontalface_default.xml",
        config_detection: Dict = {},
        config_pantilt: Dict = {},
    ):
        super().__init__(config_pantilt=config_pantilt)
        self.path_config_xml = path_config_xml
        self.config_detection = config_detection
        self.face_detection = face_Detection_Haar(
            path_config_xml, config_detection
        ).detection_one_face

class pan_Tilt_Red_Color(pan_Tilt):
    def __init__(self, config_pantilt: Dict = {}, config_detection: Dict = {}):
        super().__init__(config_pantilt=config_pantilt)
        self.config_detection = config_detection
        self.face_detection = color_Detection(**config_detection).detection_one


#! Pan Tilt and Lead Screw
class leadScrew:
    def __init__(self, motor: Motor, switch_R: Switch, switch_L: Switch) -> None:
        self.motor = motor  
        self.switch_R = switch_R
        self.switch_L = switch_L
    
    def step(self, angle: float, delay:float):
      return self.motor.step(angle, delay, self.checkStop)
  
    def checkStop(self, angle: float, sign_steps:int):
        if self.switch_R.checkClick(): 
            if sign_steps > 0 : return True
            else: return False
        elif self.switch_L.checkClick():
            if sign_steps < 0 : return True
            else: return False

class pan_Tilt_leadScrew(pan_Tilt):
  def __init__(self, config_pantilt: Dict = {}) -> None:
      super().__init__(config_pantilt)  
      self.lead_screw = leadScrew()
      self.optimization = None
      
  def control_pan_tilt(self):
    pass
  
class pan_Tilt_leadScrew_Haar(pan_Tilt_leadScrew):
    def __init__(
        self,
        path_config_xml: str = "./.model/haarcascades/haarcascade_frontalface_default.xml",
        config_detection: Dict = {},
        config_pantilt: Dict = {},
    ):
        super().__init__(config_pantilt=config_pantilt)
        self.path_config_xml = path_config_xml
        self.config_detection = config_detection
        self.face_detection = face_Detection_Haar(
            path_config_xml, config_detection
        ).detection_one_face