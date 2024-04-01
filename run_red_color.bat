@echo off
if exist .conda (
  conda activate ./.conda
  pyclean .
  python -m run_red_color
  cls
)