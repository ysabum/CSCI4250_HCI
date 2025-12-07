import cv2

# Initialize webcam
cap = cv2.VideoCapture(0)

# Load pre-trained face and eye detection models
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

FACE_COLOR = (255, 0, 0)
EYE_COLOR = (0, 255, 0)
RECTANGLE_WIDTH = 2

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Establish grayscale for better performance
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Draw rectangle around faces
    for (x, y, w, h) in faces:
        # Get region within face rectangle for use in eyes
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        # Draw rectangle around face
        #cv2.rectangle(frame, (x, y), (x+w, y+h), FACE_COLOR, RECTANGLE_WIDTH)

        # Detect eyes within face region
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            eye_gray = roi_gray[ey:ey+eh, ex:ex+ew]
            eye_color = roi_color[ey:ey + eh, ex:ex + ew]

            # Apply blur to clean up image before thresholding
            #blurred = cv2.medianBlur(eye_gray, 5)
            blurred = cv2.GaussianBlur(eye_gray, (5, 5), 0)

            # Thresholding to isolate pupil
            _, thresh = cv2.threshold(blurred, 70, 255, cv2.THRESH_BINARY_INV)

            # Find contours to detect pupils
            contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours = sorted(contours, key=lambda xl: cv2.contourArea(xl), reverse=True)

            if contours:
                (cx, cy), radius = cv2.minEnclosingCircle(contours[0])
                cv2.circle(eye_color, (int(cx), int(cy)), int(radius), EYE_COLOR, RECTANGLE_WIDTH)

            #cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), EYE_COLOR, RECTANGLE_WIDTH)

    # Display the resulting frame
    cv2.imshow('Pupil Detection', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
