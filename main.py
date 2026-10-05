import time
from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from typing import Optional
import cv2

import config
from camera import Camera
from display import Display
from gpio_handler import GPIOHandler

class State(Enum):
	PREVIEW = auto()
	COUNTDOWN = auto()
	CAPTURE = auto()
	REVIEW = auto()

def save_photo(frame) -> Optional[Path]:
	try:
		save_dir = Path(config.SAVE_DIR)
		save_dir.mkdir(parents=True, exist_ok=True)
		
		filename = datetime.now().strftime("%Y%m%d_%H%M%S") + f".{config.PHOTO_FORMAT}"
		path = save_dir / filename
		cv2.imwrite(str(path), frame)
	except Exception as e:
		print(f" Erreur lors de la sauvegarde : {e}")



def run():
	camera = Camera()
	display = Display()
	gpio = GPIOHandler()

	camera.start()

	state = State.PREVIEW
	countdown_end = 0.0  
	review_end = 0.0 
	captured_frame = None 
	flash_active = False

	while True:

		button_pressed = gpio.consume_press() 

		camera.wait_for_frame()
		surf_data = camera.surf_data

		now = time.monotonic()

		if state == State.PREVIEW:
			if surf_data is not None:
				display.show_frame(surf_data)
			if button_pressed:
				if not flash_active:
					gpio.flash_on()
					flash_active = True
				countdown_end = now + config.COUNTDOWN
				state = State.COUNTDOWN

		elif state == State.COUNTDOWN:
			remaining = int(countdown_end - now) + 1
			if surf_data is not None:
				if remaining > 0:
					display.show_countdown(surf_data, remaining)
				else:
					state = State.CAPTURE

		elif state == State.CAPTURE:
			display.show_flash()
			time.sleep(config.FLASH_ON_DELAY)
			captured_frame = camera.snapshot()
			if captured_frame is not None:
				save_photo(captured_frame)
			review_end = now + config.REVIEW_DURATION
			state = State.REVIEW

		elif state == State.REVIEW:
			if flash_active:
				gpio.flash_off()
				flash_active = False
			if captured_frame is not None:
				display.show_review(captured_frame)
			if now >= review_end:
				state = State.PREVIEW


		display.flip()
		display.tick(config.CAMERA_FPS)



if __name__ == "__main__":
	run()
