# gesture_volume_control

Control system volume using hand gesture. Uses Python, OpenCV, Mediapipe and Pycaw

MediaPipe's Hand tracking module is used to track the hand from live web cam feed using OpenCV VideoCapture. The angle between the thumb tip and the index tip is used as the volume controller. Angle range (10 - 70 degrees) is nominalized and used to set the system volume.
