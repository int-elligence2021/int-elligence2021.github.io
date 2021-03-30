from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results')
def results_page():
    return render_template('results_page.html')

@app.route('/display')
def display_page():
    return render_template('display_page.html')

if __name__ == "__main__":
    app.run(debug=True) #TODO: remove debug=True before deployment
