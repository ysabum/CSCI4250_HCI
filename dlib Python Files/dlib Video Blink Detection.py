from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import argparse
import datetime
import imutils
import time
import dlib
import cv2

def main():
    # define two constants, one for eye aspect ratio to indicate
    # blink, then a second constant for number of consecutive
    # frames the eye must be below the threshold
    EYE_AR_THRESH = 0.2
    EYE_AR_CONSEC_FRAMES = 2
    DOUBLE_BLINK_CONSEC_FRAMES = 20

    # initialize frame counters and total number of blinks
    FRAME_COUNTER = 0
    TOTAL_BLINKS = 0
    TIME_BETWEEN_BLINKS = 0
    TOTAL_DOUBLE_BLINKS = 0

    # create argument parser and then parse
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--shape-predictor", required=True, help="path to face predictor")
    #args = vars(ap.parse_args())                                      # uncomment to run with commandline arguments

    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    detector = dlib.get_frontal_face_detector()
    #predictor = dlib.shape_predictor(args["shape_predictor"])         # uncomment to run with commandline arguments
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    # grab the indices of the facial landmarks for left and right eye
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

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

            # extract left and right eye cords,
            # then use them to compute eye aspect ratios
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)

            # average the eye aspect ratio together for both eyes
            ear = (leftEAR + rightEAR) / 2.0

            # loop over (x, y) cords for the facial landmarks
            # and draw them on the image
            #for (x, y) in shape:
            #    cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

            # compute convex hull for left and right eye,
            # then visualize each of the eyes
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)


            # check if the EAR is below blink threshold,
            # if so, increment frame counter
            if ear < EYE_AR_THRESH:
                FRAME_COUNTER += 1
            else:   # otherwise, EAR is not below blink threshold
                # if the eyes were closed long enough,
                # increment number of blinks
                if FRAME_COUNTER >= EYE_AR_CONSEC_FRAMES:
                    TOTAL_BLINKS += 1

                    # check if time between blinks was below threshold,
                    # if so, double blink occurred
                    if TIME_BETWEEN_BLINKS <= DOUBLE_BLINK_CONSEC_FRAMES:
                        TOTAL_DOUBLE_BLINKS += 1
                    # reset time between blinks
                    TIME_BETWEEN_BLINKS = 0

                # reset eye frame counter
                FRAME_COUNTER = 0

                # count frames between blinks
                TIME_BETWEEN_BLINKS += 1


            # display number of blinks and current EAR
            cv2.putText(frame, "BLINKS: {}".format(TOTAL_BLINKS),
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, "EAR: {}".format(ear),
                        (250, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, "DOUBLES: {}".format(TOTAL_DOUBLE_BLINKS),
                        (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, "FRAMES: {}".format(TIME_BETWEEN_BLINKS),
                        (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # show the frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if 'q' is pressed, break loop
        if key == ord("q"):
            break

    # cleanup
    cv2.destroyAllWindows()
    vs.stop()

def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmark (x, y) cords
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # compute the euclidean distances between the
    # horizontal eye landmarks (x, y) cords
    C = dist.euclidean(eye[0], eye[3])

    # compute the eye aspect ratio (EAR)
    ear = (A + B) / (2.0 * C)

    return ear


if __name__ == "__main__":
    main()
