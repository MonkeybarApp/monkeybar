from flask import Flask
from flask import request, render_template, redirect, url_for
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
    if not query:
        return redirect(url_for('index'))
    phrases = [i for i in query.strip().split(',') if i]
    if len(phrases) == 0:
        return redirect(url_for('index'))
    result = graph.get_graph_for_phrases(phrases)
    # result is now a tuple containing node data and an edge list
    result = json.dumps((result[0], list(result[1])))
    #open('data.txt', 'w').write(result)
    #result = open('data.txt', 'r').read()
    print(result)
    print(phrases)
    return render_template('query.html', phrase=','.join(phrases), graph=result)

if __name__ == "__main__":
    app.run(debug=False)
