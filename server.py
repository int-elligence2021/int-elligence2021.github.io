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
    return render_template('results_page.html')

@app.route('/display')
def display_page():
    return render_template('display_page.html')

if __name__ == "__main__":
    app.run(debug=True) #TODO: remove debug=True before deployment
