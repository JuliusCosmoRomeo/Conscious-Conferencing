"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""
import math
import queue

import cv2
from GazeTracking.gaze_tracking import GazeTracking
from Worker import Worker

gaze = GazeTracking()

# settings

"""
video_path = "videos/zoom_fail.mp4"
frame_width = 320
frame_height = 200
y_padding = 80
frames_positions = [(0, 1), (0, 3), (2, 0), (2, 3)]
"""

video_path = "videos/checkout.mp4"
frame_width = 960
frame_height = 540
y_padding = 0
frames_positions = [(0, 0), (0, 1), (1, 0), (1, 1)]


capture = cv2.VideoCapture(video_path)

# create and start threads
threads = []
n_threads = 4

fnos = list(range(0, 3000, 10))
n_threads = 1 # n_threads is the number of worker threads to read video frame
tasks = [[] for _ in range(0, n_threads)] # store frame number for each threads
frame_per_thread = math.ceil(len(fnos) / n_threads)

tid = 0
for idx, fno in enumerate(fnos):
	tasks[math.floor(idx / frame_per_thread)].append(fno)

for _ in range(0, n_threads):
	w = Worker()
	threads.append(w)
	w.start()

results = queue.Queue(maxsize=100)
on_done = lambda x: results.put(x)
# distribute the tasks from main to worker threads
for idx, w in enumerate(threads):
	w.decode(video_path, tasks[idx], on_done)


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

    cv2.putText(frame, str(gaze.horizontal_ratio()), (90, 100), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    return frame


"""
while not capture.isOpened():
    capture = cv2.VideoCapture(video_path)
    cv2.waitKey(1000)
    print("Wait for the header")
"""
webcam = cv2.VideoCapture(0)

# if the horizontal ratio is below this value or above (1-threshold) the person is considered not attentive
attention_zone_threshold = 0.3
number_of_considered_frames = 200
cv2.namedWindow("Demo", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Demo", cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

while True:
    # We get a new frame from the capture
    #_, frames = capture.read()
    frames = results.get(timeout=5)

    _, webcam_frame = webcam.read()
    # percent by which the webcam image is resized
    scale_percent = 75

    # calculate the 50 percent of original dimensions
    width = int(webcam_frame.shape[1] * scale_percent / 100)
    height = int(webcam_frame.shape[0] * scale_percent / 100)

    # dsize
    dsize = (width, height)

    x_absolute = 0
    #img = frames[y_padding: y_padding + frame_height + height, x_absolute: frame_width * len(frames_positions)]
    img = frames

    for col, row in frames_positions:
        x_offset = row * frame_width
        y_offset = (col * frame_height) + y_padding
        frame = frames[y_offset: y_offset + frame_height, x_offset: x_offset+frame_width]
        # We send this frame to GazeTracking to analyze it

        frame = analyze_gaze(frame)
        horizontal_ratio = gaze.horizontal_ratio()
        if horizontal_ratio:
            if horizontal_ratio < attention_zone_threshold or horizontal_ratio > 1 - attention_zone_threshold:
                blur_size = int(math.pow(abs(horizontal_ratio-attention_zone_threshold)*10, 2))
                frame = cv2.blur(frame, (blur_size,blur_size))
        start_y = col * frame_height
        start_x = row * frame_width
        img[start_y: start_y + frame_height, start_x: start_x + frame_width] = frame
        #x_absolute += frame_width
    #img[frame_height:frame_height + height, 0: len(frames_positions)*frame_width] = (0,0,0)
    webcam_frame = analyze_gaze(webcam_frame)


    # resize image
    webcam_frame = cv2.resize(webcam_frame, dsize)
    img[frame_height:frame_height+height, 0: width] = webcam_frame
    #img = frames
    cv2.imshow("Demo", img)

    if cv2.waitKey(1) == 27:
        break
