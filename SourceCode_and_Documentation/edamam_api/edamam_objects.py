from py_edamam import PyEdamam

e = PyEdamam(
            nutrition_appid='1b7015b5',
            nutrition_appkey='cd0b1be36422d9ec8114e424b2a76aa9',
            recipes_appid='ed9ebd49',
            recipes_appkey='faa479368d9dd0d427347cfb1a32f2aa	',
            food_appid='a8a3b6cb',
            food_appkey='80f9ae15038451b2095a0fe982980f37')

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