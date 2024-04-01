@echo off
if exist .conda (
  conda activate ./.conda
  python -m testing_color_detection
  cls
)