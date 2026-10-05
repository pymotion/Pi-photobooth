import threading
import cv2
import numpy as np
from picamera2 import Picamera2
import config

class Camera:

	def __init__(self):
		self._picam2 = Picamera2()
		config_obj = self._picam2.create_preview_configuration(
			main={
				"size": (config.CAMERA_WIDTH, config.CAMERA_HEIGHT),
				"format": "RGB888",
			}
		)
		self._picam2.configure(config_obj)

		autofocus_controls = {}
		if config.CAMERA_AUTOFOCUS:
			from libcamera import controls as libcontrols
			autofocus_controls = {}
			autofocus_controls["AfMode"] = libcontrols.AfModeEnum.Continuous
			self._picam2.set_controls(autofocus_controls)

		try:
			self._picam2.start()
		except Exception as exc:
			print("[Caméra] Picamera2 start failed:", exc)
			

		self._surf_data = None
		self.full_frame = None
		self.lock = threading.Lock()
		self.new_frame = threading.Event()
		self.running = False
		self.thread = threading.Thread(target=self.capture_loop, daemon=True)

	def start(self):
		self.running = True
		self.thread.start()

	def stop(self):
		self.running = False
		self.thread.join(timeout=2)
		try:
			self._picam2.stop()
		except Exception:
			pass

	def wait_for_frame(self, timeout: float = 0.05) -> bool:
		return self.new_frame.wait(timeout)

	def to_surf_data(self, frame):
		preview = cv2.resize(frame, (config.PREVIEW_WIDTH, config.PREVIEW_HEIGHT), interpolation=cv2.INTER_LINEAR)
		rgb = cv2.cvtColor(preview, cv2.COLOR_BGR2RGB)
		return np.ascontiguousarray(rgb.swapaxes(0, 1))

	@property
	def surf_data(self):
		self.new_frame.clear()
		with self.lock:
			return self._surf_data.copy() if self._surf_data is not None else None

	def snapshot(self):
		with self.lock:
			return self.full_frame.copy() if self.full_frame is not None else None

	def capture_loop(self):
		while self.running:
			frame = self._picam2.capture_array()
			frame = cv2.flip(frame, 1)
			surf_data = self.to_surf_data(frame)
			with self.lock:
				self.full_frame = frame
				self._surf_data = surf_data
			self.new_frame.set()