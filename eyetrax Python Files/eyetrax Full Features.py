import os
import time
import sys

import numpy as np
import pyautogui
import pyttsx3
import pyperclip

import multiprocessing
from threading import Thread

from eyetrax.calibration import (
    run_5_point_calibration,
    run_9_point_calibration,
    run_lissajous_calibration,
)
from eyetrax.cli import parse_common_args
from eyetrax.filters import KalmanSmoother, KDESmoother, NoSmoother, make_kalman
from eyetrax.gaze import GazeEstimator
from eyetrax.utils.screen import get_screen_size
from eyetrax.utils.video import camera, iter_frames

# Functions for running TTS as thread
def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper

def speak(phrase):
    engine = pyttsx3.init()
    engine.say(phrase)
    engine.runAndWait()
    engine.stop()

def stop_speaker():
    global term
    global alive
    alive = False
    term = True
    t.join()

@threaded
def manage_process(p):
    global term
    while p.is_alive():
        if term:
            p.terminate()
            term = False
        else:
            continue

def say(phrase):
    global t
    global term
    global alive
    alive = True
    term = False
    p = multiprocessing.Process(target=speak, args=(phrase,))
    p.start()
    t = manage_process(p)


def run_demo():

    args = parse_common_args()

    filter_method = args.filter
    camera_index = args.camera
    calibration_method = args.calibration
    confidence_level = args.confidence

    gaze_estimator = GazeEstimator(model_name=args.model)

    if args.model_file and os.path.isfile(args.model_file):
        gaze_estimator.load_model(args.model_file)
        print(f"[demo] Loaded gaze model from {args.model_file}")
    else:
        if calibration_method == "9p":
            run_9_point_calibration(gaze_estimator, camera_index=camera_index)
        elif calibration_method == "5p":
            run_5_point_calibration(gaze_estimator, camera_index=camera_index)
        else:
            run_lissajous_calibration(gaze_estimator, camera_index=camera_index)

        gaze_estimator.save_model("gaze_model.pkl")

    screen_width, screen_height = get_screen_size()         # Save model to load for future runs

    if filter_method == "kalman":
        kalman = make_kalman()
        smoother = KalmanSmoother(kalman)
        smoother.tune(gaze_estimator, camera_index=camera_index)
    elif filter_method == "kde":
        kalman = None
        smoother = KDESmoother(screen_width, screen_height, confidence=confidence_level)
    else:
        kalman = None
        smoother = NoSmoother()



    with camera(camera_index) as cap:
        global alive                    # If thread is alive
        select_pause = False            # If first blink occurs
        mouse_can_move = True           # Lock mouse during interval
        CONSECUTIVE_BLINK_FRAMES = 2    # Number of frames eyes must be closed to register blink
        NO_FACE_LIMIT = 45              # Threshold of frames with closed eyes to exit program
        INTERVAL = 1.0                  # Seconds between first and second blink
        interval_start = 0.0            # Time interval was started
        blink_frame_counter = 0         # Frames eyes have been closed
        no_feature_frame_counter = 0    # Frames face is missing
        x_pred, y_pred = 0, 0           # Gaze position

        for frame in iter_frames(cap):
            features, blink_detected = gaze_estimator.extract_features(frame)   # Get face from camera

            if blink_detected:                                  # eyes closed
                blink_frame_counter += 1                              # for how long?
                print(blink_frame_counter)
                if blink_frame_counter >= NO_FACE_LIMIT:              # keep eyes closed to exit
                    print("Exit")
                    if alive:
                        stop_speaker()
                    sys.exit()
            else:
                current = time.time()
                if blink_frame_counter >= CONSECUTIVE_BLINK_FRAMES:   # blink occurred
                    if not select_pause:                        # on first blink
                        print("first blink")                   # freeze mouse position
                        mouse_can_move = False
                        select_pause = True
                        interval_start = current
                        pyautogui.moveTo(x_pred, y_pred)
                    elif select_pause and current - interval_start <= INTERVAL:    # on second blink within interval
                        print("blink two")
                        select_pause = False
                        print("CLICK")

                        # Select paragraph
                        pyautogui.click(clicks=3, interval=0.01)            # highlight text

                        # Copy to keyboard
                        pyperclip.copy("")
                        pyautogui.hotkey('ctrl', 'c')
                        time.sleep(0.01)
                        text = pyperclip.paste()

                        # Speak text
                        if alive:
                            stop_speaker()              # stop thread if already running
                            say(text)
                        else:
                            say(text)                   # start thread to use TTS

                        mouse_can_move = True
                if current - interval_start > INTERVAL:                            # too slow
                    select_pause = False
                    print("don't")                                                 # resume mouse movement
                    mouse_can_move = True

                blink_frame_counter = 0                               # reset time between blinks


            if features is not None and not blink_detected and mouse_can_move:  # face detected and free mouse
                no_feature_frame_counter = 0
                gaze_point = gaze_estimator.predict(np.array([features]))[0]    # get gaze point
                x, y = map(int, gaze_point)                                     # save gaze point to x, y
                x_pred, y_pred = smoother.step(x, y)                            # smooth gaze point

                pyautogui.moveTo(x_pred, y_pred)                                # move mouse to gaze position
                print("movem ouse")
            elif features is not None and not blink_detected and not mouse_can_move:    # face detected and locked mouse
                no_feature_frame_counter = 0
                x_pred, y_pred = pyautogui.position()                       # keep mouse in place until interval
                print("wowie zowie")
            else:
                print("no features")
                no_feature_frame_counter += 1
                x_pred = y_pred = None

                if no_feature_frame_counter >= NO_FACE_LIMIT:
                    print("Exit")
                    sys.exit()


if __name__ == "__main__":
    alive = False               # Must be initialized in global scope first
    run_demo()
