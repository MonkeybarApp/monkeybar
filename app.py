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
    phrases = query.split(',')
    result = graph.get_graph_for_phrases(phrases)
    # result is now a tuple containing node data and an edge list
    result = json.dumps((result[0], list(result[1])))
    #open('data.txt', 'w').write(result)
    #result = open('data.txt', 'r').read()
    print(result)
    return render_template('query.html', phrases=phrases, graph=result)

if __name__ == "__main__":
    app.run(debug=True)
