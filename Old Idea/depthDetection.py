import cv2
import numpy as np

cam1 = cv2.VideoCapture(0)
cam2 = cv2.VideoCapture(1)

width = 640
height = 480
cam1.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam1.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam2.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam2.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

window_size = 2
min_disp = 0
num_disp = 16*8

stereo = cv2.StereoSGBM_create(
    minDisparity=min_disp,
    numDisparities=num_disp,
    blockSize=window_size,
    P1=8 * 3 * window_size**2,
    P2=32 * 3 * window_size**2,
    disp12MaxDiff=1,
    uniquenessRatio=10,
    speckleWindowSize=100,
    speckleRange=32,
    preFilterCap=63
)

baseline_m = 0.15
focal_length_px = 4032

while True:
    ret1, frame1 = cam1.read()
    ret2, frame2 = cam2.read()

    if not ret1:
        print("USB webcam failed to capture")
        continue
    if not ret2:
        print("iPhone failed to capture")
        continue

    frame2 = cv2.resize(frame2, (width, height))

    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    disparity = stereo.compute(gray1, gray2).astype(np.float32) / 16.0

    distance_map = (focal_length_px * baseline_m) / (disparity + 1e-6)

    disp_vis = cv2.normalize(disparity, None, 0, 255, cv2.NORM_MINMAX)
    disp_vis = np.uint8(disp_vis)

    distance_vis = cv2.normalize(distance_map, None, 0, 255, cv2.NORM_MINMAX)
    distance_vis = np.uint8(distance_vis)

    intensity = 1 - (distance_map / np.max(distance_map))
    intensity_vis = (intensity * 255).astype(np.uint8)

    cv2.imshow("USB Webcam", frame1)
    cv2.imshow("iPhone Camera", frame2)
    cv2.imshow("Disparity Map", disp_vis)
    cv2.imshow("Distance Map (m)", distance_vis)
    cv2.imshow("Vibration Intensity", intensity_vis)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam1.release()
cam2.release()
cv2.destroyAllWindows()
