from py_edamam import PyEdamam

e = PyEdamam(nutrition_appid='xxx',
           nutrition_appkey='xxx',
           recipes_appid='xxx',
           recipes_appkey='xxx',
           food_appid='xxx',
           food_appkey='xxx')

for recipe in e.search_recipe("onion and chicken"):
    print(recipe)
    print(recipe.calories)
    print(recipe.cautions, recipe.dietLabels, recipe.healthLabels)
    print(recipe.url)
    print(recipe.ingredient_quantities)
    break

for nutrient_data in e.search_nutrient("2 egg whites"):
    print(nutrient_data)
    print(nutrient_data.calories)
    print(nutrient_data.cautions, nutrient_data.dietLabels,
          nutrient_data.healthLabels)
    print(nutrient_data.totalNutrients)
    print(nutrient_data.totalDaily)

for food in e.search_food("coffee and pizza"):
    print(food)
    print(food.category)