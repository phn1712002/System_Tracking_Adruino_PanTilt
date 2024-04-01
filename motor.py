from pyfirmata import Arduino

class model_RC_Servo_MG995:
    def __init__(self, board:Arduino, pin:int, angle_limit:list=[0, 180],name:str=None):
        self.board = board
        self.pin = pin
        self.name = name
        self.servo = board.get_pin(f'd:{pin}:s')
        self.angle_current = 0
        self.angle_limit = angle_limit

    def check_stop_limit(self, angle_prepare):
        return not((angle_prepare < self.angle_limit[0]) or (angle_prepare > self.angle_limit[-1]))
    
    def step(self, step_angle:float=0.1):
        angle_prepare = self.angle_current + step_angle
        if angle_prepare != self.angle_current:
            if self.check_stop_limit(angle_prepare):
                self.servo.write(angle_prepare)
                self.angle_current = angle_prepare
        return self.angle_current
    