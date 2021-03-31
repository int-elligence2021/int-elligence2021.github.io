from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=["POST", "GET"])
def results_page():
    if request.method == "POST":
        print(f"Dietary Requirements: {request.form.getlist('dietary_req')}")
        print(f"Nutritional Requirements: {request.form.getlist('nut_req')}")
        print(f"Cuisine: {request.form.get('cuisine')}")
        print(f"Dish type: {request.form.get('mealtype')}")
        print(f"Time range from {request.form.get('min-time')} to {request.form.get('max-time')} mins")
        print(f"Ingredients: {request.form.getlist('addIngred')}")
        print(f"Negative Search Ingredients: {request.form.getlist('negSearch')}")
    return render_template('results_page.html')

@app.route('/display')
def display_page():
    return render_template('display_page.html')

if __name__ == "__main__":
    app.run(debug=True) #TODO: remove debug=True before deployment
