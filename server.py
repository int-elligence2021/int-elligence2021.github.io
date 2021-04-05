from flask import Flask, render_template, request, redirect, url_for, session
from test_api import call_api, handle_selections, display_recipe

app = Flask(__name__)
app.secret_key = "int-elligence"


@app.route('/')
def index():
    ingred_error = False
    filters_error = False
    if 'error' in session:
        if session['error'] == 'ingredients':
            ingred_error = True
        else:
            filters_error = True
        session.pop('error', None)
    
    # errors result from ingredients or filters not returning any results.
    # If the results route was redirected to the index, then set conditions to display the correct error
    return render_template('index.html', ingred_error=ingred_error, filters_error=filters_error)

@app.route('/results', methods=["POST", "GET"])
def results_page():
    if request.method == "POST":
        health=request.form.getlist('dietary_req')
        health=','.join(health)

        diet=request.form.getlist('nut_req')
        diet=','.join(diet)

        cuisineType=request.form.get('cuisine')
        dishType=request.form.get('mealtype')
        
        time=f"{request.form.get('min-time')}-{request.form.get('max-time')}"
        ingredients=request.form.getlist('addIngred')
        num_ingr=len(ingredients)
        ingredients=','.join(ingredients)

        excluded=request.form.getlist('negSearch')
        excluded=','.join(excluded)

        sortby=request.form.get('sortby') #TODO: pass this into python function
        
        recipe_list = handle_selections({
            'health': health,
            'diet': diet,
            'cuisineType': cuisineType,
            'dishType': dishType,
            'time': time,
            'ingredients': ingredients,
            'num_ingr': num_ingr,
            'excluded': excluded
        })
        
        if recipe_list['error'] is not None:
            # errors exist in either ingredients selection or filters selection
            session['error'] = recipe_list['error']
            return redirect(url_for('index')) # redirects to index

        # a possible solution is to store the recipe details in a global variable (possibly in a JSON file)
        return render_template('results_page.html', recipes=recipe_list['recipes'])

    # else GET
    # for now, recipes is empty unlike the POST method so the recipe page will be empty (apart from the Carbonara)
    return render_template('results_page.html', recipes={}) 


@app.route('/display_page')
def display_page():
    recipe_name = request.args.get('recipe_name')
    recipe_info = display_recipe(recipe_name)
    return render_template('display_page.html', recipes=recipe_info)

if __name__ == "__main__":
    app.run(debug=True) #TODO: remove debug=True before deployment
