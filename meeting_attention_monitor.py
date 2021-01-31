"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
from GazeTracking.gaze_tracking import GazeTracking

gaze = GazeTracking()
video_path = "videos/zoom_fail.mp4"
capture = cv2.VideoCapture(video_path)


def analyze_gaze(frame):
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""

    if gaze.is_blinking():
        text = "Blinking"
    elif gaze.is_right():
        text = "Right"
    elif gaze.is_left():
        text = "Left"
    elif gaze.is_center():
        text = "Center"

    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    return frame


while not capture.isOpened():
    capture = cv2.VideoCapture(video_path)
    cv2.waitKey(1000)
    print("Wait for the header")

webcam = cv2.VideoCapture(0)


while True:
    # We get a new frame from the capture
    _, frames = capture.read()
    _, webcam_frame = webcam.read()
    # percent by which the webcam image is resized
    scale_percent = 50

    # calculate the 50 percent of original dimensions
    width = int(webcam_frame.shape[1] * scale_percent / 100)
    height = int(webcam_frame.shape[0] * scale_percent / 100)

    # dsize
    dsize = (width, height)

    frame_width = 320
    frame_height = 200
    y_padding = 80
    frames_positions = [(0,1), (0,3), (2,0), (2,3)]
    x_absolute = 0
    img = frames[y_padding: y_padding + frame_height + height, x_absolute: frame_width * len(frames_positions)]
    for col, row in frames_positions:
        x_offset = row * frame_width
        y_offset = (col * frame_height) + y_padding
        frame = frames[y_offset: y_offset + frame_height, x_offset: x_offset+frame_width]

        # We send this frame to GazeTracking to analyze it
        frame = analyze_gaze(frame)
        img[0: frame_height, x_absolute: x_absolute + frame_width] = frame
        x_absolute += frame_width
    img[frame_height:frame_height + height, 0: len(frames_positions)*frame_width] = (0,0,0)
    webcam_frame = analyze_gaze(webcam_frame)


    # resize image
    webcam_frame = cv2.resize(webcam_frame, dsize)
    img[frame_height:frame_height+height, 0: +width] = webcam_frame
    cv2.imshow("Demo", img)

    if cv2.waitKey(1) == 27:
        break
