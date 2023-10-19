import functools
from typing import *
import random



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
	def plancton(self) -> int:			return 0  # TODO

	def __str__(self) -> str:
		return	self.throw(*[Dice(x) for x in self.dices])		+\
				f"\tice holes:\t\t{self.ice_holes}\n"			+\
				f"\tpolar_bears:\t{self.polar_bears}\n"			+\
				f"\tfish:\t\t\t{self.fish}\n"					+\
				f"\tplancton:\t\t{self.plancton}\n"
	def __repr__(self) -> str:
		return f"<dices: {self.dices}>"



class ARound(Round):
	"""Analytical Round"""
	def __init__(self, *args, **kwargs) -> None:
		super(ARound, self).__init__(*args, **kwargs)
	@classmethod
	def from_round(cls, rnd: Round) -> object:
		a_round = cls(*rnd.dices)
		a_round.throw = rnd.throw
		return a_round

	@property
	def reciprocal(self) -> List[int]:	return [7 - x for x in self.dices]
	@property
	def sum(self) -> int:				return sum(self.dices)

	@staticmethod
	def entry(obj: object, width: int) -> str:	return str(obj).ljust(width, ' ')
	def __str__(self) -> str:
		entry = self.entry
		ih = self.ice_holes
		pb = self.polar_bears
		f = self.fish
		p = self.plancton
		return	self.throw(*[Dice(x) for x in self.dices])																	+\
				f" {' '.join([str(x) for x in self.dices])}  ===[FLIP]==>  {' '.join([str(x) for x in self.reciprocal])}\n"	+\
				f" *           | ice_holes | polar_bears | fish | plancton\n"												+\
				f" 1           | {entry(ih, 9)} | {entry(pb, 11)} | {entry(f, 4)} | {entry(p, 8)}\n"						+\
				f" ice_holes   | {entry(ih * ih, 9)} | {entry(pb * ih, 11)} | {entry(f * ih, 4)} | {entry(p * ih, 8)}\n"	+\
				f" polar_bears | {entry(ih * pb, 9)} | {entry(pb * pb, 11)} | {entry(f * pb, 4)} | {entry(p * pb, 8)}\n"	+\
				f" fish        | {entry(ih * f, 9)} | {entry(pb * f, 11)} | {entry(f * f, 4)} | {entry(p * f, 8)}\n"		+\
				f" plancton    | {entry(ih * p, 9)} | {entry(pb * p, 11)} | {entry(f * p, 4)} | {entry(p * p, 8)}\n"		+\
				f" sum: {self.sum}\n\n"



def round_gen(dice_count: int = 8, analyzed: bool = False) -> Generator[Round, None, None]:
	while True:
		args = [random.randint(1, 6) for _ in range(dice_count)]
		if analyzed:	yield ARound(*args)
		else:			yield Round(*args)
