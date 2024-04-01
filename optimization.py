import math
from typing import Any, Dict

class optimization_Control_2Motor:
  def __init__(self, step_max:float=1, step_slow:float=0.1, er_limit:float=360, region_inf:list=[0.05, 0.2, 0.3]) -> None:
    #! Check lenght region_inf
    if len(region_inf) != 3: raise ValueError("region_inf must contain exactly 3 elements")
  
    self.step_max = step_max
    self.step_slow = step_slow
    self.er_limit = er_limit
    self.region_inf = region_inf
    
    self.coef_a = (self.step_max - self.step_slow) / ((self.region_inf[-1] - self.region_inf[-2]) * self.er_limit)
    self.coef_b = self.step_max - self.coef_a * self.region_inf[-1] * self.er_limit
    self.func_linear_calc_step = lambda er: round(self.coef_a * er + self.coef_b, 1)
    self.get_sign = lambda number: math.copysign(1, number) 
  
  def function_var_speed(self, er_t):
    er_t = abs(er_t)
    step_calc = 0
    for idx, coef in enumerate(self.region_inf):
      if er_t < (coef * self.er_limit):
        if idx == 0:
          step_calc = 0
          return step_calc
        elif idx == 1:
          step_calc = self.step_slow
          return step_calc
        elif idx == 2:
          step_calc = self.func_linear_calc_step(er_t)
        return step_calc
    return self.step_max
          
  def calc_amount_correnction(self, er_motor_1, er_motor_2):
    step_motor_1 = self.function_var_speed(er_motor_1) * self.get_sign(er_motor_1)
    step_motor_2 = self.function_var_speed(er_motor_2) * self.get_sign(er_motor_2)
    return step_motor_1, step_motor_2
  
  def reset_er(self):
    return self.pid_motor_1.reset_er(), self.pid_motor_2.reset_er(),
    