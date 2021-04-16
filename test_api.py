import json
import requests
import pprint

recipe_dict = {
	'error': None,
	'recipes': []
}
app_key='faa479368d9dd0d427347cfb1a32f2aa'
app_id='ed9ebd49'
url='https://api.edamam.com/search?'

def handle_selections(req):

	query=f"q={req['ingredients']}&app_id={app_id}&app_key={app_key}&to=50"
	
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

	return call_api(query, req['num_ingr'])

def call_api(query, num_ingr):
	resp = requests.get(url + query + "&imageSize=LARGE")
	# print(url+query)
	if resp.status_code == 200:
		d=json.loads(resp.text)

		if not d['hits']:
			# no hits means no recipes
			return {'error': "ingredients"}

		for recipe in d['hits']:
			recipe['recipe']['num_missing'] = len(recipe['recipe']['ingredients']) - num_ingr
			# add recipe to dict
			recipe_dict['recipes'].append(recipe['recipe'])

		return recipe_dict
	
	# in the case of a 40x error, the filters do not match any recipes (esp. Dietary/Nut req)
	return {'error': "filters"}

def display_recipe(id):
	for recipe in recipe_dict['recipes']:
		if recipe['url'] == id:
			display_rec = {}
			nutrient = []
			for nutrients in recipe['totalNutrients']:
				sample = {}
				x = str(round(recipe['totalNutrients'][nutrients]['quantity'], 2)) + ' ' + recipe['totalNutrients'][nutrients]['unit']
				sample = {
					'label': recipe['totalNutrients'][nutrients]['label'],
					'quantity': x
				}
				nutrient.append(sample)
			display_rec = {
				"title": recipe['label'],
				"nutrient1": nutrient[0:int(len(nutrient)/2)],
				"nutrient2": nutrient[int(len(nutrient)/2) + 1:],
				"healthLabels1": recipe["healthLabels"][0:int(len(recipe["healthLabels"])/2)],
				"healthLabels2": recipe["healthLabels"][int(len(recipe["healthLabels"])/2) + 1:],
				"calories": round(recipe['calories'], 2),
				"url": recipe['url'],
				"image": recipe['image'],
				"ingredients": recipe['ingredients']
			}
			return display_rec
	return {}

# FOR TESTING PURPOSES
# recipe_list = handle_selections({
# 	'health': '',
# 	'diet': '',
# 	'cuisineType': '',
# 	'dishType': '',
# 	'time': '1%2B',
# 	'ingredients': [ 'chicken', 'pasta' ],
# 	'num_ingr': 2,
# 	'excluded': ''
# })

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

