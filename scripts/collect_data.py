#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
import time

# Polski pentesting
PL_SOURCES = [
    'https://zaufanatrzeciastrona.pl',
    'https://niebezpiecznik.pl',
    'https://sekurak.pl'
]

# EN pentesting
EN_SOURCES = [
    'https://portswigger.net/web-security/sql-injection',
    'https://portswigger.net/web-security/cross-site-scripting',
    'https://owasp.org/www-project-top-ten'
]

OUT = Path('data/raw')
OUT.mkdir(parents=True, exist_ok=True)

def scrape(url, lang):
    try:
        r = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(r.content, 'html.parser')

        for tag in soup(['script', 'style', 'nav', 'footer']):
            tag.decompose()

        title = soup.find('h1')
        title = title.get_text(strip=True) if title else 'No title'

        article = soup.find('article') or soup.find('main')
        text = article.get_text(separator='\n', strip=True) if article else ''

        return {
            'url': url,
            'title': title,
            'content': text[:3000],
            'lang': lang
        }
    except Exception as e:
        print(f"Error {url}: {e}")
        return None

# Scrape
results = []

print("Scraping PL...")
for url in PL_SOURCES[:2]:
    data = scrape(url, 'pl')
    if data:
        results.append(data)
    time.sleep(2)

print("Scraping EN...")
for url in EN_SOURCES[:3]:
    data = scrape(url, 'en')
    if data:
        results.append(data)
    time.sleep(2)

# Save
outfile = OUT / 'pentesting_data.jsonl'
with open(outfile, 'w', encoding='utf-8') as f:
    for r in results:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')

print(f"Done: {len(results)} articles → {outfile}")
