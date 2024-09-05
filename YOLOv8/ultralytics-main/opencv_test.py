import cv2

vid_cam = cv2.VideoCapture(0)

while(vid_cam.isOpened()):
    ret, image_frame = vid_cam.read()

    cv2.imshow('frame', image_frame)

    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

vid_cam.release()
cv2.destroyAllWindows()