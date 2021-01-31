import queue
import threading
import cv2


class Worker(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		self.queue = queue.Queue(maxsize=20)

	def decode(self, video_path, fnos, callback):
		self.queue.put((video_path, fnos, callback))

	def run(self):
		"""the run loop to execute frame reading"""
		video_path, fnos, on_decode_callback = self.queue.get()
		cap = cv2.VideoCapture(video_path)

		# set initial frame
		cap.set(cv2.CAP_PROP_POS_FRAMES, fnos[0])
		success = cap.grab()

		results = []
		idx, count = 0, fnos[0]
		while success:
		    if count == fnos[idx]:
		        success, image = cap.retrieve()
		        if success:
		            on_decode_callback(image)
		        else:
		            break
		        idx += 1
		        if idx >= len(fnos):
		            break
		    count += 1
		    success = cap.grab()