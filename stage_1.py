import cv2
import numpy as np

cap = cv2.VideoCapture(0) # set up video capture from default camera

while True:
    ret, frame = cap.read() # read a frame from the camera

    # converting frame into grayscale image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # setting threshold of gray image
    _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # using a findContours() function
    contours, _ = cv2.findContours(
        threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:

        # cv2.approxPloyDP() function to approximate the shape
        approx = cv2.approxPolyDP(
            contour, 0.01 * cv2.arcLength(contour, True), True)

        # finding center point of shape
        M = cv2.moments(contour)
        if M['m00'] != 0.0:
            x = int(M['m10']/M['m00'])
            y = int(M['m01']/M['m00'])

        # check if the shape is a rectangle
        if len(approx) == 4:
            # calculate the aspect ratio of the rectangle
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = float(w)/h

            # check if the aspect ratio is within a certain range to determine if it is a rectangle or a square
            if 0.95 <= aspect_ratio <= 1.05:
                cv2.putText(frame, 'Square', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            else:
                cv2.putText(frame, 'Rectangle', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            # draw a rectangle around the shape
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

        # check if the shape is a triangle
        elif len(approx) == 3:
            cv2.putText(frame, 'Triangle', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            # draw a rectangle around the shape
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

        # check if the shape is a circle
        elif len(approx) > 8:
            cv2.putText(frame, 'Circle', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            # draw a rectangle around the shape
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

    cv2.imshow('shapes', frame) # display the processed frame

    if cv2.waitKey(1) & 0xFF == ord('q'): # exit loop if 'q' is pressed
        break

cap.release() # release the capture device
cv2.destroyAllWindows
