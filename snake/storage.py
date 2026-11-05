import os

HS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "highscore.txt")


def load_high_score():
	try:
		with open(HS_FILE, "r") as f:
			return int(f.read())
	except (FileNotFoundError, ValueError):
		return 0


def save_high_score(value):
	with open(HS_FILE, "w") as f:
		f.write(str(value))