from polarbears_around_iceholes import *
from argparse import ArgumentParser, RawTextHelpFormatter
from rich import print


description =\
"""Polarbears Around Iceholes!
    This game challenges you to find the rules behind the following items (in order of difficulty):
    1. ice_holes
    2. polar_bears
    3. fish
    4. starfish
    5. eels
    6. plancton
"""

help = "Leave arguments blank to play normally!"

parser = ArgumentParser(add_help=False, description=description, formatter_class=RawTextHelpFormatter)
parser.add_argument("--help", "-h", action="help", help=help)
parser.add_argument("--save", "-s", action="store_true", default=False, help="Save results to file")
parser.add_argument("--load", "-l", action="store_true", default=False, help="Load results from file")


if __name__ == "__main__":
	args = parser.parse_args()
	if args.load:
		print("[red]Press enter to continue and Q (or ctrl+c) to exit[/red]")
		with open("games.json", "r") as file:
			games = load(file)
			file.close()

		for game in games:
			try:  # catch all keyboard interrupts
				if input(game).upper() == "Q": break
			except KeyboardInterrupt: break
		else: print("[green]End of saved games![/green]")

	else:
		games = []
		print("[red]Press enter to continue and Q (or ctrl+c) to exit[/red]")
		for rnd in round_gen():
			games.append(rnd)
			try:  # catch all keyboard interrupts
				if input(rnd).upper() == "Q": break
			except KeyboardInterrupt: break

		with open("games.json", "w") as file:
			dump(games, file)
			file.close()
