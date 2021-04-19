import json
import requests
import pprint
import math

recipe_dict = {
	'error': None,
	'recipes': [],
	'total_pages':0
}

ez_list = []
easy_ids = []

app_key='faa479368d9dd0d427347cfb1a32f2aa'
app_id='ed9ebd49'
url='https://api.edamam.com/search?'

def handle_selections(req):

	query=f"q={req['ingr_list']}&app_id={app_id}&app_key={app_key}&to=99"
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
	return call_api(query, req['ingr_list'], req['page'])

def call_api(query, ingr_list, page):
	if page is None:
		resp = requests.get(url + query)
		if resp.status_code != 200:
			# in the case of a 40x error, the filters do not match any recipes (esp. Dietary/Nut req)
			return {'error': "filters"}, None

		recipe_dict['recipes'] = []

		d=json.loads(resp.text)
		recipe_dict["total_pages"] = math.ceil(d['count'] / 21)
		if int(recipe_dict["total_pages"]) > 5:
			recipe_dict["total_pages"] = 5

		if not d['hits']:
			# no hits means no recipes
			return {'error': "ingredients"}, None

		for recipe in d['hits']:
			recipe['recipe']['num_missing'] = 0
			for ingr in recipe['recipe']['ingredients']:
				# print (ingr)
				if not any(i in ingr['text'] for i in ingr_list):
					recipe['recipe']['num_missing'] += 1
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

def easy_recipe(id):
	if id == "recipes" or id in easy_ids:
		return ez_list


def display_easyrecipe(id):
	for recipe in ez_list:
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

def easy_generator():
	easy_foods = [ 'Eggy Fried Rice', 'Burst Tomato Pasta with Charred Walnuts recipes', 'A Bite of Britain: Pancake Day' ]
	for target_recipe in easy_foods:
		easyrep_list, page = handle_selections({
		'health': '',
		'diet': '',
		'cuisineType': '',
		'dishType': '',
		'time': '1%2B',
		'ingr_list': [ target_recipe ],
		'num_ingr': 1,
		'excluded': '',
		'page': None
		})
		for recipe in easyrep_list['recipes']:
			if len(ez_list) == 3:
				break
			if recipe['label'] == target_recipe and recipe not in ez_list:
				easy_ids.append(recipe['url'])
				ez_list.append(recipe)
				break

easy_generator()