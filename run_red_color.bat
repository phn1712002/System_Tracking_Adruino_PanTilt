@echo off
if exist .conda (
  conda activate ./.conda
  python -m run_red_color
  cls
)