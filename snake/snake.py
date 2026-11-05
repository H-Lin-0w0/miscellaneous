import pygame
import random
pygame.init()

HS_FILE = "highscore.txt"
cell = 20
COLS, ROWS = 60, 40
screen = pygame.display.set_mode((1200,800))
pygame.display.set_caption("retro snake")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

snake = []
dx, dy = 0, 0
score = 0
food = (0,0)
game_over = False
paused = False
started = False

def load_high_score():
	try:
		with open(HS_FILE, "r") as f:
			return int(f.read())
	except (FileNotFoundError, ValueError):
		return 0

def save_high_score(value):
	with open(HS_FILE, "w") as f:
		f.write(str(value))

high_score = load_high_score()


def spawn_food():
	while True:
		pos = (random.randrange(COLS), random.randrange(ROWS))
		if pos not in snake:
			return pos

def get_speed():
	return min(8 + ((len(snake) - 3)//3), 15)

def reset():
	global snake, dx, dy, score, food, game_over, paused, next_dir
	snake = [(30,20),(29,20),(28,20)]
	dx, dy = 1, 0
	next_dir = (1,0)
	score = 0
	food = spawn_food()
	game_over = False
	paused = False

reset()

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN and not started:
			started = True
			continue
		if event.type == pygame.KEYDOWN:
			if game_over:
				if event.key == pygame.K_r:
					reset()
				elif event.key == pygame.K_ESCAPE:
					running = False
			else:
				if event.key == pygame.K_UP and dy == 0:
					next_dir = (0, -1)
				elif event.key == pygame.K_DOWN and dy == 0:
					next_dir = (0, 1)
				elif event.key == pygame.K_LEFT and dx == 0:
					next_dir = (-1, 0)
				elif event.key == pygame.K_RIGHT and dx == 0:
					next_dir = (1, 0)
				elif event.key == pygame.K_SPACE:
					paused = not paused

	if started and not game_over and not paused:
		dx, dy = next_dir
		head_x, head_y = snake[0]
		new_head = (head_x + dx, head_y + dy)

		out_of_bounds = not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS)
		hit_self = new_head in snake

		if out_of_bounds or hit_self:
			game_over = True
			if score > high_score:
				high_score = score
				save_high_score(high_score)
		else:
			snake.insert(0, new_head)
			if new_head == food:
				score += 1
				food = spawn_food()
			else:
				snake.pop()	

	screen.fill((0,0,0))
	for x, y in snake:
		pygame.draw.rect(screen, (0,255,0), (x * cell, y * cell, cell, cell))
	
	fx, fy = food
	pygame.draw.rect(screen, (255,0,0), (fx * cell, fy*cell, cell, cell))
	
	score_surface = font.render(f"Score: {score}", True, (255,255,255))
	speed_surface = font.render(f"Speed: {get_speed()-7}", True, (255,255,255))
	screen.blit(score_surface, (10,10))
	screen.blit(speed_surface, (10,50))
	high_surface = font.render(f"High: {high_score}", True, (255,255,255))
	screen.blit(high_surface, (10,90))

	if game_over:
		overlay = pygame.Surface((COLS * cell, ROWS * cell), pygame.SRCALPHA)
		overlay.fill((0,0,0,160))
		screen.blit(overlay, (0,0))

		center_x = COLS * cell // 2
		center_y = ROWS * cell // 2
		title = big_font.render("GAME OVER", True, (255, 80, 80))
		info = font.render(f"Final Score: {score}", True, (255,255,255))
		hint = font.render("Press R to restart, ESC to quit", True, (200,200,200))
		screen.blit(title, title.get_rect(center = (center_x, center_y - 60)))
		screen.blit(info, info.get_rect(center=(center_x, center_y)))
		screen.blit(hint, hint.get_rect(center=(center_x, center_y + 60)))

	if not started:
		overlay = pygame.Surface((COLS * cell, ROWS * cell), pygame.SRCALPHA)
		overlay.fill((0,0,0,160))
		screen.blit(overlay, (0,0))

		center_x = COLS*cell //2
		center_y = ROWS*cell // 2
		title = big_font.render("RETRO SNAKE", True, (0,240,0))
		hint = font.render("Press any key to start", True, (190, 189, 180))
		screen.blit(title, title.get_rect(center=(center_x, center_y-30)))
		screen.blit(hint, hint.get_rect(center=(center_x, center_y+30)))


	if paused and not game_over:
		center_x = COLS * cell // 2
		center_y = ROWS * cell // 2
		title = big_font.render("PAUSED", True, (255, 255, 255))
		hint = font.render("Press SPACE to continue", True, (200,200,200))
		screen.blit(title, title.get_rect(center=(center_x, center_y - 30)))
		screen.blit(hint, hint.get_rect(center=(center_x, center_y + 30)))

	pygame.display.flip()
	clock.tick(get_speed())

pygame.quit()