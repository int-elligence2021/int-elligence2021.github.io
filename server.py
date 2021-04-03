from flask import Flask, render_template, request, redirect, url_for, session
from test_api import call_api, handle_selections

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
        ingredients=','.join(ingredients)

        excluded=request.form.getlist('negSearch')
        excluded=','.join(excluded)
        
        error_type = handle_selections({
            'health': health,
            'diet': diet,
            'cuisineType': cuisineType,
            'dishType': dishType,
            'time': time,
            'ingredients': ingredients,
            'excluded': excluded
        })
        
        if error_type is not None:
            # errors exist in either ingredients selection or filters selection
            session['error'] = error_type
            return redirect(url_for('index')) # redirects to index

    return render_template('results_page.html')

@app.route('/display')
def display_page():
    return render_template('display_page.html')

if __name__ == "__main__":
    app.run(debug=True) #TODO: remove debug=True before deployment
