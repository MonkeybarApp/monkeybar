from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query/<phrase>/')
def query(phrase):
    return render_template('query.html', temp_1=phrase)

app.run(debug=True)
