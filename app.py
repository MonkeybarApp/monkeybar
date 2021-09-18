from flask import Flask
from flask import render_template
from bs4 import BeautifulSoup
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def find_links(query_phrase):
    # hardcode for now
    return [
        'https://en.wikipedia.org/wiki/World_War_I'
    ]

def extract_text(link):
    # get the html content
    req = requests.get(link)
    soup = BeautifulSoup(req.content, 'html.parser')
    text = ''
    for p in soup.find_all('p'):
        cur_text = p.get_text()
        if len(cur_text) < 50:
            continue
        ratio = len(cur_text) / len(str(p))
        if ratio <= 0.5:
            continue
        text += '\n' + cur_text
    return text

def frequency_analysis(phrase, text):
    phrase = phrase.strip().lower()
    words = text.split()
    frequency = dict()
    stop_list = ['of', 'by', 'then', 'from', 'i', 'to', 'him', 'he', 'she', 'her', 'their', 'them', 'our', 'the', 'and', 'retrieved', 'in', 'a', 'are', 'as', 'is', 'or', 'for', 'on', 'with', 'this', 'isbn', 'have', 'that', 'such', 'also', 'other', 'be', 'some', 'they', 'which', 'not', 'more', 'all', 'but', 'most', 'britannica', 'at', 'it', 'an', 'out', 'your', 'article', 'make', 'including', 'generally', 'may', 'its', 'many', 'info', 'than', 'was', 'has', 'called', 'well', 'often', 'sometimes', 'one', 'those', 'do', 'since', 'belong', 'contains', 'between', 'either', 'while', 'being', 'after', 'only', 'name', 'both', 'were', 'had', 'you', 'if', 'would', 'been', 'any', 'when', 'can', 'us', 'during', 'will', 'there', 'around', 'even', 'into', 'so', 'first', 'just', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'yes', 'no', 'use', 'used', 'these', 'against', 'became', 'who'] # to be continued
    for word in words:
        if not word.isalpha():
            continue
        if phrase in word:
            continue
        word = word.lower()
        if not word in stop_list:
            frequency[word] = 1 + frequency.get(word, 0)
    freq_list = []
    for key, value in sorted(frequency.items(), key=lambda kv: kv[1], reverse=True):
        if len(freq_list) > 20:
            break
        freq_list.append((key, value))
    return freq_list

@app.route('/query/<phrase>/')
def query(phrase):
    links = find_links(phrase)
    text = ''
    for link in links:
        text += extract_text(link) + ' '
    print(text)
    words = frequency_analysis(phrase, text)
    print(words)
    print(json.dumps(words))
    return render_template('query.html', phrase=phrase, words=json.dumps(words))

app.run(debug=True)
