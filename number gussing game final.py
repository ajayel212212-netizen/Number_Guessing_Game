#!/usr/bin/env python3
"""
Number Guessing Game (<=100 lines)
- Difficulty (easy/medium/hard)
- Hints (very close / close / warm / cold)
- Input validation and 'quit' to exit
- Simple high score saved to 'ng_highscore.json' in current directory
"""
import random, time, json
from pathlib import Path

HS_FILE = Path("ng_highscore.json")

def load_highscore():
	try:
		return json.loads(HS_FILE.read_text()).get("best")
	except Exception:
		return None

def save_highscore(score):
	try:
		HS_FILE.write_text(json.dumps({"best": score}))
	except Exception:
		pass

def choose_difficulty():
	opts = {"easy": 15, "medium": 10, "hard": 5}
	while True:
		s = input("Choose difficulty (easy/medium/hard) [medium]: ").strip().lower() or "medium"
		if s in opts:
			return opts[s]
		print("Type 'easy', 'medium', or 'hard'.")

def get_guess(low, high):
	while True:
		s = input(f"Enter your guess ({low}-{high}) or 'quit': ").strip().lower()
		if s == "quit":
			return None
		if s.isdigit():
			g = int(s)
			if low <= g <= high:
				return g
			print(f"Please pick a number between {low} and {high}.")
		else:
			print("Enter a whole number or 'quit'.")

def hint_for(secret, guess):
	d = abs(secret - guess)
	if d == 0:
		return "correct"
	if d <= 2:
		return "very close"
	if d <= 5:
		return "close"
	if d <= 10:
		return "warm"
	return "cold"

def play_round():
	low, high = 1, 100
	secret = random.randint(low, high)
	tries = choose_difficulty()
	print(f"I chose a number between {low} and {high}. You have {tries} guesses.")
	start = time.time()
	attempts = 0
	while attempts < tries:
		g = get_guess(low, high)
		if g is None:
			print("Quitting this round.")
			return None
		attempts += 1
		h = hint_for(secret, g)
		if h == "correct":
			elapsed = int(time.time() - start)
			score = max(0, 100 - attempts * 2 - elapsed)
			print(f"Correct! {g} in {attempts} guesses, {elapsed}s. Score: {score}")
			return score
		dir_msg = "Too low." if g < secret else "Too high."
		print(f"{dir_msg} ({h}) — guesses left: {tries - attempts}")
	print(f"Out of guesses! The number was {secret}.")
	return 0

def main():
	print("Number Guessing Game")
	best = load_highscore()
	if best is not None:
		print(f"Current high score: {best}")
	while True:
		result = play_round()
		if result is None:
			break
		if best is None or result > best:
			best = result
			save_highscore(best)
			print(f"New high score: {best} (saved)")
		if input("Play again? (y/n): ").strip().lower() not in ("y", "yes"):
			break
	print("Thanks for playing!")

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("\nGoodbye.")

