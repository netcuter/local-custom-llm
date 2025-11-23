#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
import time

# Polski pentesting - konkretne artykuły
PL_SOURCES = [
    'https://sekurak.pl/sql-injection-podstawy/',
    'https://sekurak.pl/xss-cross-site-scripting-podstawy/',
    'https://niebezpiecznik.pl/post/jak-zlamac-haslo-do-wifi/',
    'https://zaufanatrzeciastrona.pl/post/bezpieczenstwo-aplikacji-webowych/',
    'https://sekurak.pl/burp-suite-podstawy-pracy/',
]

# EN pentesting - więcej artykułów
EN_SOURCES = [
    'https://owasp.org/www-project-top-ten',
    'https://owasp.org/Top10/A01_2021-Broken_Access_Control/',
    'https://owasp.org/Top10/A03_2021-Injection/',
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
for url in PL_SOURCES:
    data = scrape(url, 'pl')
    if data:
        results.append(data)
    time.sleep(1)

print("Scraping EN...")
for url in EN_SOURCES:
    data = scrape(url, 'en')
    if data:
        results.append(data)
    time.sleep(1)

# Save
outfile = OUT / 'pentesting_data.jsonl'
with open(outfile, 'w', encoding='utf-8') as f:
    for r in results:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')

print(f"Done: {len(results)} articles → {outfile}")
