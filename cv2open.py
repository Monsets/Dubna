import json
import imutils
import time
import numpy as np
import cv2

from utils import construct_arguments, point_in_box
from boxes import lower_box, upper_box

x_min = 279
y_max = 500
x_max = 517
y_min = 320

with open('answers.json') as f:
    files = json.load(f)



passanger_is_coming = False
passangers_count = 0

args = construct_arguments()

debugging = args.get('debugging')

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
    #vs = VideoStream(src=0).start()
    time.sleep(2.0)
    print("Specify video (-v path)")
    exit(1)

# otherwise, we are reading from a video file
else:
    vs = cv2.VideoCapture(args["video"])

# initialize the first frame in the video stream
firstFrame = None

# loop over the frames of the video
while True:
    # grab the current frame and initialize the occupied/unoccupied
    # text
    frame = vs.read()
    frame = frame if args.get("video", None) is None else frame[1]

    # if the frame could not be grabbed, then we have reached the end
    # of the video
    if frame is None:
        break

    # resize the frame, convert it to grayscale, and blur it
    frame = frame[y_min:y_max, x_min: x_max]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    #gray = cv2.convertScaleAbs(gray)

    if firstFrame is None:
        firstFrame = gray
        continue

    # compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 15, 255, cv2.THRESH_BINARY)[1]

    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=30)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)

    #not supported on jupiter
    cnts = imutils.grab_contours(cnts)

    # loop over the contours
    for c in cnts:
        #epsilon = cv2.arcLength(c, True)
        #approx = cv2.approxPolyDP(c, 2, True)
        #c = np.array(c)
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < args["min_area"]:
            continue

        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)

        #if detection observed in lower box
        if point_in_box((x + (w / 2), y + (h / 2)), lower_box):
            passanger_is_coming = True

            if debugging:
                print('he is coming ')

        #in upper box and hes coming
        if passanger_is_coming and  point_in_box((x + (w / 2), y + (h/ 2)), upper_box):
            passangers_count += 1
            passanger_is_coming = False

            if debugging:
                print('he\' s came')

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)


    if debugging:
        #printing lower and upper boxes
        cv2.rectangle(frame, lower_box['start'], lower_box['end'], (0, 0, 255), 2)
        cv2.rectangle(frame, upper_box['start'], upper_box['end'], (255, 0, 0), 2)

        # show the frame and record if the user presses a key
        cv2.imshow("Thresh", thresh)
        cv2.imshow("Frame Delta", frameDelta)
        cv2.moveWindow('Frame Delta', 500, 20)
        cv2.imshow("Security Feed", frame)
        cv2.moveWindow('Security Feed', 800, 20)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
            break

        #s key to stop video
        if key == ord('s'):
            time.sleep(10)

        time.sleep(.01)


    firstFrame = gray

# cleanup the camera and close any open windows
vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()
print(passangers_count)
