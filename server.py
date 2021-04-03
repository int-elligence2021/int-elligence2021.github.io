from flask import Flask, render_template, request, redirect, url_for
from test_api import call_api, handle_selections
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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
        
        valid = handle_selections({
            'health': health,
            'diet': diet,
            'cuisineType': cuisineType,
            'dishType': dishType,
            'time': time,
            'ingredients': ingredients,
            'excluded': excluded
        })
        
        if not valid:
            # go back to index
            # display some kind of error message on webpage (maybe activate a warning modal through a javascript getElementById )
            return redirect(url_for('index'))

    return render_template('results_page.html')

@app.route('/display')
def display_page():
    return render_template('display_page.html')

if __name__ == "__main__":
    app.run(debug=True) #TODO: remove debug=True before deployment
