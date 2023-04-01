import cv2 as cv
import time
from emailling import send_email

# start the video capture option
video = cv.VideoCapture(0)
time.sleep(1)

# sets the frame
first_frame = None
status_list = []

while True:
    status = 0

    # starts taking the video and checks if it is taking the video
    check, frame = video.read()

    # makes the frame to a gray color and then
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray_frame_gau = cv.GaussianBlur(gray_frame, (21, 21), 0)

    # checks if the first_frame is empty and then stores the frame for comparison
    if first_frame is None:
        first_frame = gray_frame_gau

    # used to compare the old frame with the new frames
    delta_frame = cv.absdiff(first_frame, gray_frame_gau)


    thresh_frame = cv.threshold(delta_frame, 65, 255, cv.THRESH_BINARY)[1]
    dil_frame = cv.dilate(thresh_frame, None, iterations=3)
    cv.imshow("My video", dil_frame)

    contours, check = cv.findContours(dil_frame, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # checks for objects and highlights them
    for contour in contours:
        if cv.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv.boundingRect(contour)
        rect = cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        if rect.any():
            status = 1

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        send_email()
    print(status_list)

    cv.imshow("video", frame)
    key = cv.waitKey(1)

    if key == ord("q"):
        break

video.release()
