import json
import requests
import pprint

def handle_selections(req):
	app_key='faa479368d9dd0d427347cfb1a32f2aa'
	app_id='ed9ebd49'

	query=f"q={req['ingredients']}&app_id={app_id}&app_key={app_key}&to=100"
	
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

	return call_api(query, req['num_ingr'], req['page'])

def call_api(query, num_ingr, page):
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
			'recipes': [],
		}
		for recipe in d['hits']:
			recipe['recipe']['num_missing'] = len(recipe['recipe']['ingredients']) - num_ingr
			# add recipe to dict
			recipe_dict['recipes'].append(recipe['recipe'])
		
		recipe_dict['start'] = int(page)*20 - 20
		recipe_dict['end'] = int(page)*20

		return recipe_dict
	
	# in the case of a 40x error, the filters do not match any recipes (esp. Dietary/Nut req)
	return {'error': "filters"}

def sort_by(recipes, sort_option):
	def sort_missing(r):
			return r['num_missing']
	def sort_alpha(r):
			return r['label']
	def sort_time_ascending(r):
			return r['totalTime']
	def sort_time_descending(r):
			return r['totalTime']
	def sort_calories(r):
			return r['calories']
		
	if sort_option == 'missing':
		return sorted(recipes, key=sort_missing)
	elif sort_option == 'alpha':
		return sorted(recipes, key=sort_alpha)
	elif sort_option == 'ascending':
		return sorted(recipes, key=sort_time_ascending)
	elif sort_option == 'descending':
		return sorted(recipes, key=sort_time_descending, reverse=True)
	elif sort_option == 'calories':
		return sorted(recipes, key=sort_calories)
	else:
		return recipes
