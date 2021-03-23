from py_edamam import Edamam

e = Edamam(nutrition_appid='1b7015b5',
           nutrition_appkey='cd0b1be36422d9ec8114e424b2a76aa9',
           recipes_appid='ed9ebd49',
           recipes_appkey='faa479368d9dd0d427347cfb1a32f2aa	',
           food_appid='a8a3b6cb',
           food_appkey='80f9ae15038451b2095a0fe982980f37')
           
print(e.search_nutrient("1 large apple"))
print(e.search_recipe("onion and chicken"))
print(e.search_food("coke"))