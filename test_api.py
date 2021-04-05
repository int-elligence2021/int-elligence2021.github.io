import json
import requests

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
	resp = requests.get(url + query)
	print(url+query)
	if resp.status_code == 200:
		d=json.loads(resp.text)

		if not d['hits']:
			# no hits means no recipes
			return {'error': "ingredients"}

		for recipe in d['hits']:
			recipe['recipe']['num_missing'] = len(recipe['recipe']['ingredients']) - num_ingr
			# add recipe to dict
			recipe_dict['recipes'].append(recipe['recipe'])
			# print(recipe['recipe']['label'])
			# for ingr in recipe['recipe']['ingredients']:
			# 	print(f"\t{ingr['text']}")
			# print('\n')
		return recipe_dict
	
	# in the case of a 40x error, the filters do not match any recipes (esp. Dietary/Nut req)
	return {'error': "filters"}

def display_recipe(label):
	for recipe in recipe_dict['recipes']:
		if recipe['label'] == label:
			print(label)
			return recipe
	return {}

# print("Hello!")
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

# res = display_recipe("Italian Chicken Pasta Salad")
# print(res)