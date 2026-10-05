import time
import config

from gpiozero import Button, OutputDevice,Device
from gpiozero.pins.lgpio import LGPIOFactory

Device.pin_factory = LGPIOFactory()

class GPIOHandler:
	def __init__(self):
		self._button_pressed = False

		self.btn   = Button(config.BUTTON_PIN, bounce_time=config.BUTTON_BOUNCE, pull_up=True)
		self.flash = OutputDevice(config.FLASH_PIN, active_high=True, initial_value=False) \
						if config.FLASH_PIN is not None else None
		self.btn.when_pressed = self._on_button_press


	def consume_press(self) -> bool:
		if self._button_pressed:
			self._button_pressed = False
			return True
		return False

	def flash_on(self):
		self.flash_pulse()

	def flash_off(self):
		self.flash_pulse()

	def flash_pulse(self):
		if self.flash:
			self.flash.on()
			time.sleep(config.FLASH_PULSE_DURATION)
			self.flash.off()

	def close(self):
		self.btn.close()
		if self.flash:
			self.flash.close()

	def _on_button_press(self, channel=None):
		self._button_pressed = True
