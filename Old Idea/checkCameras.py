import cv2

camera_indices = [0, 1, 2]
for idx in camera_indices:
    cap = cv2.VideoCapture(idx)
    ret, frame = cap.read()
    if ret:
        cv2.imshow(f"Camera {idx}", frame)
        print(f"Camera {idx} works")
        cv2.waitKey(1000)
    cap.release()
cv2.destroyAllWindows()
