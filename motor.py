from pyfirmata import Arduino
from tools import delay_microseconds
import numpy as np


# Interfaces
class Motor:
    def __init__(self, board: Arduino, pin: int, name=None):
        self.board = board
        self.name = name
        self.pin = pin

class model_RC_Servo_MG995(Motor):
    def __init__(
        self, board: Arduino, pin: int, angle_limit: list = [0, 180], name: str = None
    ):
        super().__init__(board, pin, name)
        self.servo = board.get_pin(f"d:{pin}:s")
        self.angle_current = 0
        self.angle_limit = angle_limit

    def check_stop_limit(self, angle_prepare):
        return not (
            (angle_prepare < self.angle_limit[0])
            or (angle_prepare > self.angle_limit[-1])
        )

    def step(self, step_angle: float = 0.1):
        angle_prepare = self.angle_current + step_angle
        if angle_prepare != self.angle_current:
            if self.check_stop_limit(angle_prepare):
                self.servo.write(angle_prepare)
                self.angle_current = angle_prepare
        return self.angle_current

class Model_17HS3401(Motor):
    def __init__(
        self,
        board: Arduino,
        step_pin: int,
        dir_pin: int,
        div_step=1,
        pos_dir=0,
        name=None,
    ):

        # Env
        super().__init__(board, 0, name)
        self.HIGHT = 1
        self.LOW = 0

        self.dir_pin = board.get_pin(f"d:{dir_pin}:o")
        self.step_pin = board.get_pin(f"d:{step_pin}:o")
        self.div_step = div_step
        self.pos_dir = pos_dir

        # Save info step motor
        self.history_step_angle = 0
        self._step_angle_conts = 1.8
        self.step_angle = self._step_angle_conts / div_step

    def step(self, angle, delay=0.0001, checkStop=None):

        # Convert angle, i
        if angle.__class__ is tuple:
            angle, i = angle
        elif angle.__class__ is int:
            i = 1

        # Calc steps of motor with angle and get dir
        steps = angle / self.step_angle
        direction = None
        sign_steps = np.sign(steps)
        steps = np.abs(int(steps))
        if sign_steps == True:
            direction = self.pos_dir
        else:
            direction = not self.pos_dir

        # Create checkPoint show break in steps
        in_progress_break = False

        # Control direction
        self.dir_pin.write(direction)
        for idx in range(steps):
            # Control Motor
            self.step_pin.write(self.HIGHT)
            delay_microseconds(delay)
            self.step_pin.write(self.LOW)
            delay_microseconds(delay)

            # Calc angle future
            temp_angle = self.history_step_angle + self.step_angle * i * sign_steps

            # Check stop
            if not checkStop is None and idx % self.step_skip == 0:
                if checkStop(angle=temp_angle, sign_steps=sign_steps) == True:
                    in_progress_break = True

            # Break out
            if not in_progress_break:
                self.history_step_angle = temp_angle
            else:
                break

        # Exit checkStop and create reset checkStop
        if not checkStop is None:
            checkStop(exit=True)
        delay_microseconds(delay)

        return self.history_step_angle, in_progress_break
