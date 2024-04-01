from typing import Any, List
from math import sqrt

class Point:
  def __init__(self, x:float=0, y:float=0) -> None:
    self.coordinates = (x, y)
    self.x = x 
    self.y = y
  
  def __add__(self, other):
    return Point(self.x + other.x, self.y + other.y)
  
  def __sub__(self, other):
    return Point(self.x - other.x, self.y - other.y)
  
  def __truediv__(self, other:float):
    return Point(self.x/other, self.y/other)
  
  def __str__(self) -> str:
    return str(self.coordinates)
  
class Rectangle:
  def __init__(self, list_point:List) -> None:
    if len(list_point) != 4: raise ValueError("list_point must contain exactly 4 elements")
    
    self.point_base = list_point[0]
    self.list_point = list_point
    self.point_center = self.calc_point_center()
    self.vertical = None
    self.horizontal = None
    self.area = self.calc_area()
    
  def calc_point_center(self):
    point = sum_point(self.list_point)/len(self.list_point)
    return point

  def calc_area(self):
    for idx in range(1, len(self.list_point)):
      vector = self.list_point[0] - self.list_point[idx]
      if vector.x == 0:
          self.vertical = length_2_point(self.list_point[0], self.list_point[idx])
      elif vector.y == 0:
          self.horizontal = length_2_point(self.list_point[0], self.list_point[idx])
      else: pass
    return self.vertical * self.horizontal
  
  def __sub__(self, other):
    return self.point_center - other.point_center
  
  def __str__(self) -> str:
    return str(self.list_point)
  
  def calc_er_xy_2_rec(self, rec):
    er = self.point_center - rec.point_center
    return er.x, er.y

def length_2_point(point_a:Point, point_b:Point):
  return sqrt((point_a.x-point_b.x)**2 + (point_a.y-point_b.y)**2)

def sum_point(list_point:List):
  sum  = Point()
  for point in list_point:
    sum = sum + point
  return sum