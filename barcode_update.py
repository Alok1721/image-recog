import cv2
import numpy as np

barcode_image = cv2.imread("bar5.jpg")
gray_image = cv2.cvtColor(barcode_image, cv2.COLOR_BGR2GRAY)
_, threshold_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(threshold_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
stripe_threshold = 50
binary_representation = ""

for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    
    if w < 10:
        continue
    
    if w >= stripe_threshold:
        binary_representation += "1"
        cv2.drawContours(barcode_image, [contour], -1, (0, 255, 0), 2)
        cv2.rectangle(barcode_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    else:
        binary_representation += "0"
        cv2.drawContours(barcode_image, [contour], -1, (0, 0, 255), 2)

binary_representation = binary_representation[::-1]  # Reverse the binary representation
print("Binary representation:", binary_representation)

cv2.imshow("Threshold Image", threshold_image)
cv2.imshow("Image with Contours and Rectangles", barcode_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
