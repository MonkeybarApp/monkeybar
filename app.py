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
    print('got here')
    query = request.args.get('q', None)
    if query is None:
        return redirect(url_for('index'))
    result = graph.get_graph_for_phrase(query)
    result = (list(result[0]), list(result[1]))
    result = json.dumps(result)
    print(result)
    return render_template('query.html', phrase=query, graph=result)

if __name__ == "__main__":
    app.run(debug=True)
