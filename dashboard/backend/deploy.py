import cortex
import pickle
import json
import numpy as np

class NumpyEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, np.ndarray):
			return obj.tolist()
		
		return json.JSONEncoder.default(self, obj)

def convert(o):
	if isinstance(o, np.int64):
		return int(o)

class PythonPredictor:
	def __init__(self, config):
		filePath = "model.p"
		self.model = pickle.load(open(filePath, "rb"))

	def predict(self, query_params, payload):
		typeOfQuery = query_params.get("type")

		if typeOfQuery == "dropdowns":
			filePath = "dropdowns/" + "country" + ".p"
			countries = pickle.load(open(filePath, "rb"))

			filePath = "dropdowns/" + "director" + ".p"
			directors = pickle.load(open(filePath, "rb"))

			filePath = "dropdowns/" + "genre" + ".p"
			genres = pickle.load(open(filePath, "rb"))

			filePath = "dropdowns/" + "main_cast_1" + ".p"
			main_cast_1 = pickle.load(open(filePath, "rb"))

			filePath = "dropdowns/" + "main_cast_2" + ".p"
			main_cast_2 = pickle.load(open(filePath, "rb"))

			filePath = "dropdowns/" + "main_cast_3" + ".p"
			main_cast_3 = pickle.load(open(filePath, "rb"))

			data = {
				"countries": dict(zip(countries.classes_, countries.transform(countries.classes_))),
				"directors": dict(zip(directors.classes_, directors.transform(directors.classes_))),
				"genres": dict(zip(genres.classes_, genres.transform(genres.classes_))),
				"main_cast_1": dict(zip(main_cast_1.classes_, main_cast_1.transform(main_cast_1.classes_))),
				"main_cast_2": dict(zip(main_cast_2.classes_, main_cast_2.transform(main_cast_2.classes_))),
				"main_cast_3": dict(zip(main_cast_3.classes_, main_cast_3.transform(main_cast_3.classes_)))
			}

			return json.dumps(data, default=convert)

		data = [
			payload["year"],
			payload["genre"],
			payload["director"],
			payload["main_cast_1"],
			payload["main_cast_2"],
			payload["main_cast_3"],
			payload["budget"],
			payload["country"],
			payload["runtime"]
		]

		response = {
			"prediction": self.model.predict([data])[0]
		}

		return json.dumps(response, cls=NumpyEncoder)
