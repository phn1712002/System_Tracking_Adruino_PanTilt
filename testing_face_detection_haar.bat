@echo off
if exist .conda (
  conda activate ./.conda
  python -m testing_face_detection_haar
  cls
)