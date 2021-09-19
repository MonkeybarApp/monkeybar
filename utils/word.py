import asyncio
import httpx
from unidecode import unidecode
import re
from .data import common_words

banned_str = ["'s", '\n']

async def clean_text(content):
    content = unidecode(content).lower()
    for i in banned_str:
        content = content.replace(i, ' ')

    content = re.sub(r'[^a-z]', ' ', content)

    wordlist = [i for i in content.split(' ') if len(i) > 1 and i not in common_words]
    return list(filter(('').__ne__, wordlist))

async def process_wikipedia_article(article):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get('https://en.wikipedia.org/w/api.php', params={
                'action': 'query',
                'prop': 'extracts',
                'titles': article,
                'explaintext': '1',
                'exsectionformat': 'plain',
                'format': 'json',
                'formatversion': '2',
            })
            response.raise_for_status()
        except httpx.HTTPError as exc:
            return []

    return await clean_text(response.json()['query']['pages'][0]['extract'])

async def get_wordlists_for_phrase(phrase):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get('https://en.wikipedia.org/w/api.php', params={
                'action': 'query',
                'list': 'search',
                'srsearch': phrase,
                'format': 'json',
                'formatversion': '2',
            })
            response.raise_for_status()

            data = response.json()
        except httpx.HTTPError as exc:
            return []


    pages = [i['title'] for i in data['query']['search']]
    # if len(pages) > 15: pages = pages[:15]
    wordlists = await asyncio.gather(*[process_wikipedia_article(i) for i in pages])

    return wordlists

async def get_wordlists_for_phrases(phrases):
    wordlist_list =  await asyncio.gather(*[get_wordlists_for_phrase(i) for i in phrases])

    wordlists = []
    for i in wordlist_list:
        wordlists.extend(i)

    return wordlists
