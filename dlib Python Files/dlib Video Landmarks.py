from imutils.video import VideoStream
from imutils import face_utils
import datetime
import time
import numpy as np
import argparse
import imutils
import dlib
import cv2
import scipy

# create argument parser and then parse
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True, help="path to face predictor")
# args = vars(ap.parse_args())                                      # uncomment to run with commandline arguments

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
detector = dlib.get_frontal_face_detector()
# predictor = dlib.shape_predictor(args["shape_predictor"])         # uncomment to run with commandline arguments
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# initialize the video stream and give the camera time to warmup
vs = VideoStream(src=0).start()
time.sleep(2.0)

# loop over frames in video stream
while True:
    # grab frame, resize to have a maximum width of 400px
    # and convert to grayscale
    frame = vs.read()
    frame = imutils.resize(frame, width=400)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect faces in the grayscale frame
    rects = detector(gray, 0)

    # loop over face detections
    for rect in rects:
        # determine facial landmarks for face region,
        # then convert the (x, y) landmark cords to a NumPy array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        # loop over (x, y) cords for the facial landmarks
        # and draw them on the image
        for (x, y) in shape:
            cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

    # show the frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if 'q' is pressed, break loop
    if key == ord("q"):
        break

# cleanup
cv2.destroyAllWindows()
vs.stop()
