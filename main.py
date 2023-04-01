import cv2 as cv
import time
from emailling import send_email
from glob import glob

# start the video capture option
video = cv.VideoCapture(0)
time.sleep(1)

# sets the frame
first_frame = None
status_list = []

# used for the number of images captured
count = 1

while True:
    # resets the status of the object on every iteration
    status = 0

    # starts taking the video and checks if it is taking the video
    check, frame = video.read()

    # makes the frame to a gray color and then makes it blurry to be able to blur out the background
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray_frame_gau = cv.GaussianBlur(gray_frame, (21, 21), 0)

    # checks if the first_frame is empty and then stores the frame for comparison
    if first_frame is None:
        first_frame = gray_frame_gau

    # used to compare the old frame with the new frames
    delta_frame = cv.absdiff(first_frame, gray_frame_gau)

    # focuses the white color on the object and blacks out the background
    thresh_frame = cv.threshold(delta_frame, 65, 255, cv.THRESH_BINARY)[1]

    # makes sure that the object only is white
    dil_frame = cv.dilate(thresh_frame, None, iterations=2)
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

            # stores images captured from the frame
            cv.imwrite(f"images/{count}.png", frame)
            # updates the number of images taken
            count += 1

            # stores all images in a list and chooses the one in the middle to send it
            all_images = glob("images/*.png")
            size = int(len(all_images)/2)
            image = all_images[size]

    # stores the status of the object in a list to check if it is still in frame
    status_list.append(status)
    status_list = status_list[-2:]

    # checks if an object is still in frame then sends an email if not
    if status_list[0] == 1 and status_list[1] == 0:
        send_email(image)
    print(status_list)

    # presents the colored normal frame
    cv.imshow("video", frame)
    key = cv.waitKey(1)

    # quits the program when q is pressed
    if key == ord("q"):
        break

# deletes the video capture
video.release()
