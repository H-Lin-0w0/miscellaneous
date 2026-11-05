import pygame
from settings import cell, COLS, ROWS

pygame.init()

screen = pygame.display.set_mode((COLS * cell, ROWS * cell))
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)


def draw_board(game):
	screen.fill((0,0,0))
	for x, y in game.snake:
		pygame.draw.rect(screen, (0,255,0), (x * cell, y * cell, cell, cell))

	fx, fy = game.food
	pygame.draw.rect(screen, (255,0,0), (fx * cell, fy * cell, cell, cell))

	score_surface = font.render(f"Score: {game.score}", True, (255,255,255))
	speed_surface = font.render(f"Speed: {game.get_speed() - 7}", True, (255,255,255))
	high_surface = font.render(f"High: {game.high_score}", True, (255,255,255))
	screen.blit(score_surface, (10,10))
	screen.blit(speed_surface, (10,50))
	screen.blit(high_surface, (10,90))


def draw_dim_background():
	overlay = pygame.Surface((COLS * cell, ROWS * cell), pygame.SRCALPHA)
	overlay.fill((0,0,0,160))
	screen.blit(overlay, (0,0))


def draw_start_screen():
	draw_dim_background()
	center_x = COLS * cell // 2
	center_y = ROWS * cell // 2
	title = big_font.render("RETRO SNAKE", True, (0,240,0))
	hint = font.render("Press any key to start", True, (190,189,180))
	screen.blit(title, title.get_rect(center=(center_x, center_y - 30)))
	screen.blit(hint, hint.get_rect(center=(center_x, center_y + 30)))


def draw_pause_screen():
	draw_dim_background()
	center_x = COLS * cell // 2
	center_y = ROWS * cell // 2
	title = big_font.render("PAUSED", True, (255,255,255))
	hint = font.render("Press SPACE to continue", True, (200,200,200))
	screen.blit(title, title.get_rect(center=(center_x, center_y - 30)))
	screen.blit(hint, hint.get_rect(center=(center_x, center_y + 30)))


def draw_game_over_screen(game):
	draw_dim_background()
	center_x = COLS * cell // 2
	center_y = ROWS * cell // 2
	title = big_font.render("GAME OVER", True, (255,80,80))
	info = font.render(f"Final Score: {game.score}", True, (255,255,255))
	hint = font.render("Press R to restart, ESC to quit", True, (200,200,200))
	screen.blit(title, title.get_rect(center=(center_x, center_y - 60)))
	screen.blit(info, info.get_rect(center=(center_x, center_y)))
	screen.blit(hint, hint.get_rect(center=(center_x, center_y + 60)))


def draw(game):
	draw_board(game)
	if game.game_over:
		draw_game_over_screen(game)
	elif not game.started:
		draw_start_screen()
	elif game.paused:
		draw_pause_screen()