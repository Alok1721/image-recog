import cv2
import numpy as np

from pyzbar import pyzbar


cap = cv2.VideoCapture(0) # set up video capture from default camera
prev_shape = None

while True:
    ret, frame = cap.read() # read a frame from the camera

    # converting frame into grayscale image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # setting threshold of gray image
    _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # using a findContours() function
    contours, _ = cv2.findContours(
        threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    current_shape = None

    for contour in contours:

        # cv2.approxPloyDP() function to approximate the shape
        approx = cv2.approxPolyDP(
            contour, 0.01 * cv2.arcLength(contour, True), True)

        # finding center point of shape
        M = cv2.moments(contour)
        if M['m00'] != 0.0:
            x = int(M['m10']/M['m00'])
            y = int(M['m01']/M['m00'])

        # putting shape name at center of each shape
        if len(approx) == 3:
            cv2.putText(frame, 'Triangle', (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            current_shape = 'Triangle'

        elif len(approx) == 4:
            # Check if it's a square or rectangle
            (x, y, w, h) = cv2.boundingRect(contour)
            ar = w / float(h)

            if 0.95 <= ar <= 1.05:
                cv2.putText(frame, 'Square', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                current_shape = 'Square'
            else:
                cv2.putText(frame, 'Rectangle', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                current_shape = 'Rectangle'

        elif len(approx) > 4:
            cv2.putText(frame, 'Circle', (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            current_shape = 'Circle'

        else:
            continue

        # draw a green line between similar shapes
        if prev_shape == current_shape:
            cv2.line(frame, (x, y), (prev_x, prev_y), (0, 255, 0), 2)

        prev_shape = current_shape
        prev_x = x
        prev_y = y

    cv2.imshow('shapes', frame) # display the processed frame

    if cv2.waitKey(1) & 0xFF == ord('q'): # exit loop if 'q' is pressed
        break

cap.release() # release the capture device

#cap = cv2.VideoCapture(0) # set up video capture from default camera

while True:
    ret, frame = cap.read() # read a frame from the camera

    # converting frame into grayscale image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # using pyzbar to decode barcodes
    barcodes = pyzbar.decode(gray)

    for barcode in barcodes:
        # extract the barcode data and type
        barcode_data = barcode.data.decode('utf-8')
        barcode_type = barcode.type

        # draw a rectangle around the barcode
        x, y, w, h = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # put the barcode data and type on the frame
        cv2.putText(frame, 'Type: {}'.format(barcode_type), (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(frame, 'Data: {}'.format(barcode_data), (x, y + h + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow('Barcode Reader', frame) # display the processed frame

    if cv2.waitKey(1) & 0xFF == ord('q'): # exit loop if 'q' is pressed
        break

cap.release() # release the capture device
cv2.destroyAllWindows() # destroy all windows

