import wikipedia
import requests
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

def get_wordlist_for_article(article_title):
    print(article_title)
    try:
        return clean_text(wikipedia.page(title=article_title).content)
    except wikipedia.exceptions.PageError:
        return []
