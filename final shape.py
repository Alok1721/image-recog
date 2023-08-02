import cv2
import numpy as np

iriun_webcam_index = 1  # Replace with the correct index
cap = cv2.VideoCapture(iriun_webcam_index)

min_contour_area = 1000  # Minimum contour area to consider

while True:
    ret, frame = cap.read() # read a frame from the camera

    # converting frame into grayscale image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # setting threshold of gray image
    _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # using a findContours() function
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # finding center point of shape
        M = cv2.moments(contour)
        if M['m00'] != 0.0:
            x = int(M['m10'] / M['m00'])
            y = int(M['m01'] / M['m00'])

            # Calculate contour area
            area = cv2.contourArea(contour)

            # Skip contours with small area
            if area < min_contour_area:
                continue

            # cv2.approxPloyDP() function to approximate the shape
            approx = cv2.approxPolyDP(contour, 0.04 * cv2.arcLength(contour, True), True)

            # check if the shape is a rectangle
            if len(approx) == 4:
                # calculate the aspect ratio of the rectangle
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = float(w) / h

                # check if the aspect ratio is within a certain range to determine if it is a rectangle or a square
                if 0.95 <= aspect_ratio <= 1.05:
                    cv2.putText(frame, 'Square', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                else:
                    cv2.putText(frame, 'Rectangle', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

                # draw a rectangle around the shape
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # check if the shape is a triangle
            elif len(approx) == 3:
                cv2.putText(frame, 'Triangle', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

                # draw a rectangle around the shape
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # check if the shape is a circle
            else:
                perimeter = cv2.arcLength(contour, True)
                circularity = 4 * np.pi * (area / (perimeter * perimeter))
                if circularity > 0.8:  # A circularity threshold to differentiate from other shapes
                    # adjust the bounding rectangle to be centered around the shape's center point
                    x, y, w, h = cv2.boundingRect(contour)
                    x_centered = int(x + w / 2)
                    y_centered = int(y + h / 2)
                    x_centered -= int(w / 4)
                    y_centered -= int(h / 4)

                    cv2.putText(frame, 'Circle', (x_centered, y_centered), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

                    # draw a rectangle around the shape
                    cv2.rectangle(frame, (x_centered, y_centered), (x_centered + int(w / 2), y_centered + int(h / 2)), (0, 255, 0), 2)

    cv2.imshow('shapes', frame) # display the processed frame

    if cv2.waitKey(1) & 0xFF == ord('q'): # exit loop if 'q' is pressed
        break

cap.release() # release the capture device
cv2.destroyAllWindows()
