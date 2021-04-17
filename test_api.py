import json
import requests
import pprint
import math

recipe_dict = {
	'error': None,
	'recipes': [],
	'total_pages':0
}

app_key='faa479368d9dd0d427347cfb1a32f2aa'
app_id='ed9ebd49'
url='https://api.edamam.com/search?'

def handle_selections(req):

	query=f"q={req['ingredients']}&app_id={app_id}&app_key={app_key}&to=99"
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

	query+="&imageSize=LARGE"
	return call_api(query, req['num_ingr'], req['page'])

def call_api(query, num_ingr, page):
	if page is None:
		resp = requests.get(url + query)
		if resp.status_code != 200:
			# in the case of a 40x error, the filters do not match any recipes (esp. Dietary/Nut req)
			return {'error': "filters"}, None

		d=json.loads(resp.text)
		recipe_dict["total_pages"] = math.ceil(d['count'] / 21)
		if int(recipe_dict["total_pages"]) > 5:
			recipe_dict["total_pages"] = 5

		if not d['hits']:
			# no hits means no recipes
			return {'error': "ingredients"}, None

		for recipe in d['hits']:
			recipe['recipe']['num_missing'] = len(recipe['recipe']['ingredients']) - num_ingr
			recipe['recipe']['calories'] = round(recipe['recipe']['calories'], 2)
			# add recipe to dict
			recipe_dict['recipes'].append(recipe['recipe'])
		page = 1

	recipe_dict['start'] = (int(page)-1)*21
	recipe_dict['end'] = int(page)*21

	return recipe_dict, page

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
				"calories": recipe['calories'],
				"url": recipe['url'],
				"image": recipe['image'],
				"ingredients": recipe['ingredients']
			}
			return display_rec
	return {}

def easy_recipe():
	ez_list = []
	easy_foods = [ 'Eggy Fried Rice', 'Tomato Basil Pasta', 'Banana Pancakes' ]
	for target_recipe in easy_foods:
		# print(target_recipe)
		easyrep_list, page = handle_selections({
		'health': '',
		'diet': '',
		'cuisineType': '',
		'dishType': '',
		'time': '1%2B',
		'ingredients': [ target_recipe ],
		'num_ingr': 1,
		'excluded': '',
		'page': None
		})
		# print(recipe_list)
		for recipe in easyrep_list['recipes']:
			if recipe['label'] == target_recipe:
				# print(recipe)
				ez_list.append(recipe)
				break
	return ez_list

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
			return int(r['calories'])
		
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
