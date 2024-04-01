@echo off
if exist .conda (
  conda activate ./.conda
  pyclean .
  python -m testing_face_detection_haar
  cls
)