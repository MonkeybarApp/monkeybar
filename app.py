from flask import Flask
from flask import request, render_template, redirect, url_for
from bs4 import BeautifulSoup
import requests
import json
from utils import graph

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', None)
    if query is None:
        return redirect(url_for('index'))
    return render_template('query.html', graph=graph.get_graph_for_phrase(query))

if __name__ == "__main__":
    app.run(debug=True)
