import json
import requests

url='https://api.edamam.com/search?'
app_key='faa479368d9dd0d427347cfb1a32f2aa'
app_id='ed9ebd49'

resp = requests.get(url + \
	f'q=[flour, eggs, milk]&app_id={app_id}&app_key={app_key}')
d=json.loads(resp.text)
for item in d['hits']:
	print(item['recipe']['healthLabels'])