import functools
import json

from .game import Round



class json_encoder(json.JSONEncoder):
	def default(self: object, obj: object) -> dict | str:
		if type(obj) == Round:
			return {"dices": obj.dices}
		return json.dumps(obj)


class json_decoder(json.JSONDecoder):
	def __init__(self, *args, **kwargs) -> None:
		self.orig_obj_hook = kwargs.pop("object_hook", None)
		super(json_decoder, self).__init__(*args, object_hook=self.default, **kwargs)

	def default(self: object, data: dict) -> object:
		try:	return Round(*data["dices"])
		except:	pass
		return data


dump = functools.partial(json.dump, cls=json_encoder)
load = functools.partial(json.load, cls=json_decoder)
dumps = functools.partial(json.dumps, cls=json_encoder)
loads = functools.partial(json.loads, cls=json_decoder)
