import functools
from typing import *
import random
import math



class Dice:
	@staticmethod
	def printable(value: int) -> Generator[str, None, None]:
		filler = ("   " if value != 6 else " ")
		sides = filler.join(list('x' * (value // 2)))
		yield " _______ "
		yield f"| {sides.ljust(5, ' ')} |"
		yield f"|   {'x' if value % 2 else ' '}   |"
		yield f"| {sides.rjust(5, ' ')} |"
		yield " ¯¯¯¯¯¯¯ "

	def __init__(self, value: int) -> None:
		self.value = value
		self.gen = Dice.printable(self.value)

	def __next__(self) -> str:
		try: return next(self.gen)
		except StopIteration:
			self.gen = Dice.printable(self.value)
			return ""  # restart the gen



def throw_dices(*dices: Dice, width: int = 4, sep: str = " ") -> str:
	ret = ""
	while sample := random.sample(dices, min(len(dices), width)):
		dices = [dice for dice in dices if dice not in sample]
		while "" not in (line := [next(x) for x in sample]):
			ret += f"{sep.join(line)}\n"
	return ret



class Round:
	def __init__(self, *dices: int, width: int = 4, sep: str = " ") -> None:
		self.dices = dices
		self.throw = functools.partial(throw_dices, width=width, sep=sep)

	@property
	def ice_holes(self) -> int:			return len([x for x in self.dices if x % 2])
	@property
	def polar_bears(self) -> int:		return sum([x - 1 for x in self.dices if x % 2])
	@property
	def fish(self) -> int:				return sum([7 - x for x in self.dices if x % 2])
	@property
	def eels(self) -> int:				return sum([math.ceil((7 - x) / 3) for x in self.dices if x in [1, 2, 4]])
	@property
	def starfish(self) -> int:			return len([x for x in self.dices if x not in [2, 5]])
	@property
	def plancton(self) -> int:			return sum([(x + 1) * 7 - x for x in self.dices if not x % 2])


	def __str__(self) -> str:
		return	self.throw(*[Dice(x) for x in self.dices])		+\
				f"\tice holes:\t\t{self.ice_holes}\n"			+\
				f"\tpolar_bears:\t{self.polar_bears}\n"			+\
				f"\tfish:\t\t\t{self.fish}\n"					+\
				f"\teels:\t\t\t{self.eels}\n"					+\
				f"\tstarfish:\t\t{self.starfish}\n"				+\
				f"\tplancton:\t\t{self.plancton}\n"
	def __repr__(self) -> str:
		return f"<dices: {self.dices}>"



def round_gen(dice_count: int = 8) -> Generator[Round, None, None]:
	while True:
		yield Round(
			*[random.randint(1, 6) for _ in range(dice_count)]
		)
