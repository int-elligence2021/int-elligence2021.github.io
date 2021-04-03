import json
import requests

def handle_selections(req):
	app_key='faa479368d9dd0d427347cfb1a32f2aa'
	app_id='ed9ebd49'

	query=f"q={req['ingredients']}&app_id={app_id}&app_key={app_key}"
	
	if req['diet'] != '':
		query=f"{query}&diet={req['diet']}"

	if req['health'] != '':
		query=f"{query}&health={req['health']}"

	if req['cuisineType'] != '':
		query=f"{query}&cuisineType={req['cuisineType']}"

	if req['dishType'] != '':
		query=f"{query}&dishType={req['dishType']}"

	query=f"{query}&time={req['time']}"

	if req['excluded'] != '':
		query=f"{query}&excluded={req['excluded']}"

	return call_api(query)

def call_api(query):
	url='https://api.edamam.com/search?'
	resp = requests.get(url + query)
	print(url+query)
	if resp.status_code == 200:
		d=json.loads(resp.text)

		if not d['hits']:
			# no hits means no recipes
			return {'error': "ingredients"}

		recipe_dict = {
			'error': None,
			'recipes': []
		}
		for recipe in d['hits']:
			# add recipe to dict
			recipe_dict['recipes'].append(recipe['recipe']['label']) # have only added recipe name as of now

			print(recipe['recipe']['label'])
			for ingr in recipe['recipe']['ingredients']:
				print(f"\t{ingr['text']}")
			print('\n')

		return recipe_dict
	
	# in the case of a 40x error, the filters do not match any recipes (esp. Dietary/Nut req)
	return {'error': "filters"}
