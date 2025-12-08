# CSCI4250 HCI Project: Webcam-based Text System
This project presents an accessibility-oriented application that enables hands-free interaction with digital text through webcam-based eye-tracking. The long-term objective is to establish glance-based navigation as a standardized and seamless operating environment. With anticipated improvements in low-latency processing and high-resolution webcams, the system could progress from a reading assistant to a fully gaze-controlled operating system. Users would be able to perform complex tasks, such as detailed editing or digital signing, and manage applications solely through nuanced eye movements and gesture patterns, thereby enhancing accessibility and transparency in computing interfaces.

## Implementation Milestones
### Milestone 1: Lo-Fi Prototype & Initial Gaze Tracking Demo

* Created a paper prototype illustrating the intended interaction flow
* Developed an early gaze-tracking demo using OpenCV to detect eye movement and estimate gaze direction
* Produced a video walkthrough demonstrating the prototype concept
* Established the GitHub repository and project board

### Milestone 2: Paper Prototype of the Full Application

* Completed a more detailed paper prototype outlining the full system UI and interaction steps
* Frontend team began constructing a Windows application mockup and planning the PyQt interface
* Continued exploring the required APIs and libraries to support backend functionality
* Completed a second milestone video showing how the paper prototype would function in practice

### Milestone 3: Early GUI + Improved Eye Tracking

* Implemented an initial PyQt GUI allowing users to test eye-tracking from within the interface
* Backend team began integrating Dlib to improve accuracy of gaze tracking
* Combined the working gaze-tracking demo with the prototype GUI to test early end-to-end interaction
* Completed milestone video demonstrating gaze tracking through the new GUI

### Milestone 4: Core Feature Implementation

* Implemented all major backend features:
  * Real-time gaze-controlled cursor movement
  * Double-blink detection triggering a triple-click
  * Automatic text-to-speech reading of highlighted text
* Continued improvements to gaze stability using calibration steps and smoothing
* Produced an implementation video showcasing the working system and all core interactions

## Links
[Project Board](https://github.com/users/ysabum/projects/3)

## Python Resources Referenced
### Currently Referenced
https://github.com/ck-zhang/EyeTrax  
https://github.com/nateshmbhat/pyttsx3/issues/138  
https://pypi.org/project/pyttsx3/  
https://pypi.org/project/pyperclip/  
https://pyautogui.readthedocs.io/en/latest/mouse.html#mouse-clicks  
https://pyttsx3.readthedocs.io/en/latest/engine.html#the-engine-factory  

### Formerly Referenced / Obsolete
https://medium.com/analytics-vidhya/haar-cascades-explained-38210e57970d  
https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html  
https://medium.com/@amit25173/opencv-eye-tracking-aeb4f1b46aa3
https://pyimagesearch.com/2017/04/03/facial-landmarks-dlib-opencv-python/
https://pyimagesearch.com/2017/04/17/real-time-facial-landmark-detection-opencv-python-dlib/
https://pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/
