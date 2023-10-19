from polarbears_around_iceholes import *


dat = ("""
113334 -> 31 !!!
112234 -> 69
122234 -> 88
112335 -> 19 !!!
123456 -> 93 !!!
223356 -> 81
111234 -> 26 !!!
124555 -> 26 !!!
134556 -> 74
113355 -> 0 !!!!!!
123334 -> 50
223456 -> 69
115566 -> 86 !!!
112355 -> 19 !!!
223355 -> 38 !!!
234666 -> 179 ???
114456 -> 105 !!!
122666 -> 167 !!!
223336 -> 81
244466 -> 184 ???
115566 -> 86
222666 -> 186 ???
223456 -> 112 ???
222246 -> 150 ???
344455 -> 93
113356 -> 43 ???
122334 -> 69
"""
.replace(" ", "")
.replace("!", "")
.replace("?", "")
.split("\n"))
dat = [x.split("->") for x in dat if x]


if __name__ == "__main__":
	for dices, plancton in dat:
		print(ARound(*[int(x) for x in list(dices)], width=6), f" plancton: {plancton}", sep="\n", end="\n\n")

	for rnd in round_gen():
		input(rnd)

	#gen = round_gen()
	#with open("games.json", "w") as file:
	#	dump([next(gen) for _ in range(100)], file)
	#	file.close()
	#with open("games.json", "r") as file:
	#	games = load(file)
	#	file.close()


