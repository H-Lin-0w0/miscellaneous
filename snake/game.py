import pygame
import random
from settings import cell, COLS, ROWS
from storage import load_high_score, save_high_score
from render import draw

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("retro snake")


class Game:
	def __init__(self):
		self.high_score = load_high_score()
		self.started = False
		self.running = True
		self.reset()

	def reset(self):
		self.snake = [(30,20),(29,20),(28,20)]
		self.dx, self.dy = 1, 0
		self.next_dir = (1, 0)
		self.score = 0
		self.food = self.spawn_food()
		self.game_over = False
		self.paused = False

	def spawn_food(self):
		while True:
			pos = (random.randrange(COLS), random.randrange(ROWS))
			if pos not in self.snake:
				return pos

	def get_speed(self):
		return min(8 + ((len(self.snake) - 3) // 3), 15)

	def handle_key(self, key):
		if not self.started:
			self.started = True
			return
		if self.game_over:
			if key == pygame.K_r:
				self.reset()
			elif key == pygame.K_ESCAPE:
				self.running = False
			return
		if key == pygame.K_UP and self.dy == 0:
			self.next_dir = (0, -1)
		elif key == pygame.K_DOWN and self.dy == 0:
			self.next_dir = (0, 1)
		elif key == pygame.K_LEFT and self.dx == 0:
			self.next_dir = (-1, 0)
		elif key == pygame.K_RIGHT and self.dx == 0:
			self.next_dir = (1, 0)
		elif key == pygame.K_SPACE:
			self.paused = not self.paused

	def move_snake(self):
		self.dx, self.dy = self.next_dir
		head_x, head_y = self.snake[0]
		new_head = (head_x + self.dx, head_y + self.dy)

		out_of_bounds = not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS)
		hit_self = new_head in self.snake

		if out_of_bounds or hit_self:
			self.game_over = True
			if self.score > self.high_score:
				self.high_score = self.score
				save_high_score(self.high_score)
		else:
			self.snake.insert(0, new_head)
			if new_head == self.food:
				self.score += 1
				self.food = self.spawn_food()
			else:
				self.snake.pop()


game = Game()

while game.running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game.running = False
		if event.type == pygame.KEYDOWN:
			game.handle_key(event.key)

	if game.started and not game.game_over and not game.paused:
		game.move_snake()

	draw(game)
	pygame.display.flip()
	clock.tick(game.get_speed())

pygame.quit()