import requests
from googlesearch import search
import wikipedia
from bs4 import BeautifulSoup
from unidecode import unidecode
import re
from .data import common_words

banned_str = ["'s", '\n']

def clean_text(content):
    content = unidecode(content).lower()
    for i in banned_str:
        content = content.replace(i, ' ')

    content = re.sub(r'[^a-z]', ' ', content)

    wordlist = [i for i in content.split(' ') if len(i) > 1 and i not in common_words]
    return list(filter(('').__ne__, wordlist))

def get_wordlist_for_url(url):
    resp = requests.get(url)

    if resp.status_code != requests.codes.ok:
        return []

    content = ""

    soup = BeautifulSoup(resp.text, 'html.parser')
    for p_elm in soup.find_all('p'):
        if len(p_elm.text) > len(p_elm)/2:
            content += p_elm.text

    if len(content) > 10:
        return clean_text(content)
    else:
        return []


def get_wordlists_for_phrase(phrase):
    wordlists = []

    # for url in search(phrase, stop=0):
    #     wordlists.append(get_wordlist_for_url(url))

    for article in wikipedia.search(phrase, results=15):
        print(article)
        try:
            wordlists.append(clean_text(wikipedia.page(title=article).content))
        except wikipedia.exceptions.WikipediaException:
            pass

    return wordlists
