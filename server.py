from flask import Flask, render_template, request, redirect, url_for, session
from test_api import call_api, handle_selections

# saves recipe list and form inputs after every POST method
data = {}

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
        diet=request.form.getlist('nut_req')

        cuisineType=request.form.get('cuisine')
        dishType=request.form.get('mealtype')
        
        time=f"{request.form.get('min-time')}-{request.form.get('max-time')}"
        ingredients=request.form.getlist('addIngred')
        num_ingr=len(ingredients)
        excluded=request.form.getlist('negSearch')

        sortby=request.form.get('sortby')

        recipe_list = handle_selections({
            'health': ','.join(health),
            'diet': ','.join(diet),
            'cuisineType': cuisineType,
            'dishType': dishType,
            'time': time,
            'ingredients': ','.join(ingredients),
            'num_ingr': num_ingr,
            'excluded': ','.join(excluded)
        })
        
        if recipe_list['error'] is not None:
            # errors exist in either ingredients selection or filters selection
            session['error'] = recipe_list['error']
            return redirect(url_for('index')) # redirects to index

        # save recipe and form data so it is saved until the next successful POST method
        data['recipes'] = recipe_list['recipes']
        data['form_data'] = formRequest(request.form)

        return render_template('results_page.html', recipes=recipe_list['recipes'], form_data=formRequest(request.form))

    # else request.method == GET
    # (clicked back button from display page)
    return render_template('results_page.html', recipes=data['recipes'], form_data=data['form_data']) 


@app.route('/display')
def display_page():
    return render_template('display_page.html', form_data=formRequest(request.form))


# saves the user data input into the forms and copies the data onto the next page
# so that inputs don't need to be entered again if modifications are to be made
def formRequest(form):
    return {
        'diet_req': form.getlist('dietary_req'),
        'nut_req': form.getlist('nut_req'),
        'cuisineType': form.get('cuisine'),
        'dishType': form.get('mealtype'),
        'ingredients': form.getlist('addIngred'),
        'excluded': form.getlist('negSearch'),
        'sort': form.get('sortby')
    }


if __name__ == "__main__":
    app.run(port=0)
