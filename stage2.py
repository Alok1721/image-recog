import cv2
from pyzbar import pyzbar

cap = cv2.VideoCapture(0) # set up video capture from default camera

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
