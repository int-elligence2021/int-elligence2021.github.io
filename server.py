from flask import Flask, render_template, request, redirect, url_for, session
from test_api import call_api, handle_selections, display_recipe, sort_by, easy_recipe, display_easyrecipe
import requests

# saves recipe list and form inputs after every POST method
data = {}

app = Flask(__name__)
app.secret_key = "int-elligence"


@app.route('/')
def index():
    data['form_data'] = formRequest(request.form)
    # data['recipes'] = {}
    recipes = easy_recipe("recipes")
    session['url'] = url_for('index') # stores url of current page so it can be redirected to in the case of ingredient/filter errors
    e = errorCheck()    
    return render_template('index.html', ingred_error=e['i'], filters_error=e['f'], recipes=recipes)


@app.route('/results', methods=["POST", "GET"])
def results_page():
    if request.method == "POST":

        health=request.form.getlist('dietary_req')
        diet=request.form.get('nut_req')

        cuisineType=request.form.get('cuisine')
        dishType=request.form.get('mealtype')
        
        time=f"{request.form.get('min-time')}-{request.form.get('max-time')}"
        ingredients=request.form.getlist('addIngred')
        num_ingr=len(ingredients)
        excluded=request.form.getlist('negSearch')

        page=request.form.get('page')

        recipe_list, page = handle_selections({
            'health': health,
            'diet': diet,
            'cuisineType': cuisineType,
            'dishType': dishType,
            'time': time,
            'ingredients': ','.join(ingredients),
            'ingr_list': ingredients,
            'excluded': ','.join(excluded),
            'page': page
        })
        
        if recipe_list['error'] is not None:
            # errors exist in either ingredients selection or filters selection
            session['error'] = recipe_list['error']
            return redirect(session['url']) # redirects to previous page


        sorted_list=sort_by(recipe_list['recipes'], request.form.get('sortby'))

        # save recipe and form data so it is saved until the next successful POST method
        data['recipes'] = sorted_list[recipe_list['start']:recipe_list['end']]
        data['form_data'] = formRequest(request.form)
        data['page'] = f"page{page}"
        data['total_pages'] = recipe_list['total_pages']


    # if request.method == GET then come here directly
    # (clicked back button from display page)
    session['url'] = url_for('results_page')
    e = errorCheck()
    print(f"User data: {data['form_data']}")
    return render_template('results_page.html', recipes=data['recipes'],
        form_data=data['form_data'], ingred_error=e['i'], filters_error=e['f'],
        page=data['page'], total_pages=[x+2 for x in range(data['total_pages']-1)]) 


@app.route('/display')
def display_page():
    recipe_id = request.args.get('recipe_id')
    recipe_info = display_recipe(recipe_id)
    from_index = easy_recipe(recipe_id)
    back = url_for('results_page')

    if from_index:
        recipe_info = display_easyrecipe(recipe_id)
        back = url_for('index')

    if recipe_info["image"][-4:] == '.jpg' and recipe_info["image"][-6:-4] != "-l":
        if (requests.head(recipe_info['image'][:-4] + "-l" + recipe_info["image"][-4:]).status_code == 200):
            recipe_info['image'] = recipe_info['image'][:-4] + "-l" + recipe_info["image"][-4:]
    else:
        if (requests.head(recipe_info['image'] + "-l").status_code == 200):
            recipe_info['image'] = recipe_info['image'] + "-l"

    return render_template('display_page.html', display=recipe_info, back_url=back)


# saves the user data input into the forms and copies the data onto the next page
# so that inputs don't need to be entered again if modifications are to be made
def formRequest(form):
    return {
        'diet_req': form.getlist('dietary_req'),
        'nut_req': form.get('nut_req'),
        'cuisineType': form.get('cuisine'),
        'dishType': form.get('mealtype'),
        'ingredients': form.getlist('addIngred'),
        'excluded': form.getlist('negSearch'),
        'sort': form.get('sortby')
    }


# if any errors occur when looking for recipes in the API, they are stored in the session
# errorCheck returns the status of errors in the file in a dictionary
def errorCheck():
    ingred_error = False
    filters_error = False
    if 'error' in session:
        if session['error'] == 'ingredients':
            ingred_error = True
        else:
            filters_error = True
        session.pop('error', None)

    return {'i': ingred_error, 'f': filters_error}


if __name__ == "__main__":
    app.run(port=0)
