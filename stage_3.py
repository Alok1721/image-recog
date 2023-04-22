import cv2
import numpy as np
from pyzbar import pyzbar

cap = cv2.VideoCapture(0)

prev_shape = None
prev_center = None

while True:
    ret, frame = cap.read()

    # detect shapes
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        M = cv2.moments(contour)
        if M['m00'] != 0.0:
            x = int(M['m10']/M['m00'])
            y = int(M['m01']/M['m00'])

        if len(approx) == 3:
            shape_name = 'Triangle'
            color = (0, 255, 0)
        elif len(approx) == 4:
            shape_name = 'Rectangle'
            color = (0, 0, 255)
        elif len(approx) == 5:
            shape_name = 'Pentagon'
            color = (255, 0, 0)
        elif len(approx) == 6:
            shape_name = 'Hexagon'
            color = (255, 255, 0)
        else:
            shape_name = 'Circle'
            color = (255, 0, 255)

        # draw shape on frame
        cv2.drawContours(frame, [contour], 0, color, 5)
        cv2.putText(frame, shape_name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # draw line between same shapes
        if prev_shape is not None and shape_name == prev_shape:
            cv2.line(frame, prev_center, (x, y), color, 2)

        prev_shape = shape_name
        prev_center = (x, y)

    # detect barcodes
    barcodes = pyzbar.decode(frame)

    for barcode in barcodes:
        barcode_type = barcode.type
        barcode_data = barcode.data.decode('utf-8')
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(frame, f'{barcode_type}: {barcode_data}', (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # display the frame
    cv2.imshow("Shape and Barcode Scanner", frame)

    # exit loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release video capture and close all windows
cap.release()
cv2.destroyAllWindows()
