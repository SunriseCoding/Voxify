import cv2
import numpy

cap = cv2.VideoCapture(0)
ret, frame = cap.read()

if ret:
    while True:
        key = cv2.waitKey(1)
        if key != -1 and key != 27:
            print("Key pressed: ", key)
        elif key == 27:
            break
        cap.release()

        cv2.imshow("Test", frame)

cv2.destroyAllWindows()