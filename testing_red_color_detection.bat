@echo off
if exist .conda (
  conda activate ./.conda
  pyclean .
  python -m testing_red_color_detection
  cls
)