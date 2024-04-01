@echo off
if exist .conda (
  conda activate ./.conda
  pyclean .
  python -m run_haar
  cls
)