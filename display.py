import numpy as np
import cv2
import pygame
import config


class Display:

	def __init__(self):
		pygame.init()

		flags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
		self._screen = pygame.display.set_mode((0, 0), flags)
		pygame.display.set_caption("PhotoBooth")
		
		self.cx, self.cy = self._screen.get_rect().center
	
		self._font_big   = pygame.font.SysFont(None, 300)
		self._font_small = pygame.font.SysFont(None, 80)
		self._clock      = pygame.time.Clock()
		self._surf       = pygame.Surface((config.PREVIEW_WIDTH, config.PREVIEW_HEIGHT))


	def show_frame(self, surf_data):
		pygame.surfarray.blit_array(self._surf, surf_data)
		pygame.transform.scale(self._surf, self._screen.get_size(), self._screen)

	def show_countdown(self, surf_data, number: int):
		self.show_frame(surf_data)
		label  = self._font_big.render(str(number), True, (255, 255, 255))
		self._screen.blit(label,  label.get_rect(center=(self.cx, self.cy)))

	def show_flash(self):
		self._screen.fill((255, 255, 255))
		pygame.display.flip()

	def show_review(self, bgr_frame):
		preview   = cv2.resize(bgr_frame, (config.PREVIEW_WIDTH, config.PREVIEW_HEIGHT),
							   interpolation=cv2.INTER_LINEAR)
		rgb       = cv2.cvtColor(preview, cv2.COLOR_BGR2RGB)
		surf_data = np.ascontiguousarray(rgb.swapaxes(0, 1))
		self.show_frame(surf_data)
		msg    = self._font_small.render("Photo sauvegardée !", True, (255, 255, 255))
		self._screen.blit(msg,    msg.get_rect(center=(self.cx, self.cy - 80)))

	def flip(self):
		pygame.display.flip()

	def tick(self, fps: int = 30):
		self._clock.tick(fps)

	def close(self):
		pygame.quit()

	def should_quit(self) -> bool:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return True
		return False

