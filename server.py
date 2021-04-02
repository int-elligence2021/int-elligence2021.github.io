from flask import Flask, render_template, request
from test_api import call_api, handle_selections
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=["POST", "GET"])
def results_page():
    if request.method == "POST":
        health=request.form.getlist('dietary_req')
        diet=request.form.getlist('nut_req')
        cuisineType=request.form.get('cuisine')
        if cuisineType=='All Cuisine':
            cuisineType=[]
        dishType=request.form.get('mealtype')
        if dishType=='All Dish Types':
            dishType=[]
        time=f"{request.form.get('min-time')}-{request.form.get('max-time')}"
        ingredients=request.form.getlist('addIngred')
        excluded=request.form.getlist('negSearch')
        
        handle_selections({
            'health': health,
            'diet': diet,
            'cuisineType': cuisineType,
            'dishType': dishType,
            'time': time,
            'ingredients': ingredients,
            'excluded': excluded
        })
    return render_template('results_page.html')

@app.route('/display')
def display_page():
    return render_template('display_page.html')

if __name__ == "__main__":
    app.run(port=0) #TODO: remove debug=True before deployment
