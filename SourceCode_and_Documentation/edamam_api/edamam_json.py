from py_edamam import Edamam

e = Edamam(nutrition_appid='xxx',
           nutrition_appkey='xxx',
           recipes_appid='xxx',
           recipes_appkey='xxx',
           food_appid='xxx',
           food_appkey='xxx')
           
print(e.search_nutrient("1 large apple"))
print(e.search_recipe("onion and chicken"))
print(e.search_food("coke"))