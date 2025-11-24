#!/usr/bin/env python3
"""
Collect writeups from HTB, TryHackMe, VulnHub, CTFs and other sources
"""

import json
import time
from pathlib import Path
from typing import List, Dict
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import re

OUT = Path('data/raw')
OUT.mkdir(parents=True, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}


# ===== HTB Writeup Sources =====
HTB_WRITEUP_BLOGS = [
    'https://0xdf.gitlab.io/',  # Very comprehensive
    'https://rana-khalil.gitbook.io/hack-the-box-oscp-preparation/',
    'https://blog.techorganic.com/',
    'https://www.youtube.com/@ippsec/videos',  # Video writeups (we'll get descriptions)
]

# Popular HTB writeup GitHub repos
HTB_GITHUB_REPOS = [
    'Hackplayers/hackthebox-writeups',
    'Bengman/OSCP-Preparations',
    'xct/xct.github.io',
]


def fetch_0xdf_writeups(limit=50):
    """Fetch writeups from 0xdf.gitlab.io"""
    print("\n[HTB] Fetching from 0xdf.gitlab.io...")

    data = []
    base_url = 'https://0xdf.gitlab.io'

    try:
        r = requests.get(base_url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.content, 'html.parser')

        # Find HTB writeup links
        links = soup.find_all('a', href=re.compile(r'/\d{4}/\d{2}/\d{2}/htb-'))

        print(f"  Found {len(links)} writeup links, fetching {min(limit, len(links))}...")

        for link in tqdm(links[:limit]):
            try:
                url = link.get('href')
                if not url.startswith('http'):
                    url = base_url + url

                r = requests.get(url, headers=HEADERS, timeout=15)
                soup = BeautifulSoup(r.content, 'html.parser')

                # Remove unwanted elements
                for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
                    tag.decompose()

                title = soup.find('h1')
                title_text = title.get_text(strip=True) if title else 'HTB Writeup'

                article = soup.find('article') or soup.find(class_='post-content')
                if article:
                    content = article.get_text(separator='\n', strip=True)

                    if len(content) > 500:
                        data.append({
                            'url': url,
                            'title': title_text,
                            'content': content[:15000],
                            'source': 'htb_0xdf',
                            'type': 'writeup',
                            'lang': 'en'
                        })

                time.sleep(1.5)

            except Exception as e:
                pass

        print(f"  ✅ Collected {len(data)} writeups from 0xdf")

    except Exception as e:
        print(f"  ❌ Error: {e}")

    return data


def fetch_rana_khalil_writeups():
    """Fetch from Rana Khalil's OSCP prep"""
    print("\n[HTB] Fetching from Rana Khalil's GitBook...")

    data = []
    base_url = 'https://rana-khalil.gitbook.io/hack-the-box-oscp-preparation'

    try:
        r = requests.get(base_url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.content, 'html.parser')

        # This is a GitBook, structure may vary
        # Try to find links to individual writeups
        links = soup.find_all('a', href=True)

        writeup_links = []
        for link in links:
            href = link.get('href', '')
            if 'writeup' in href.lower() or 'linux' in href or 'windows' in href:
                if href.startswith('/'):
                    writeup_links.append(base_url + href)
                elif href.startswith('http'):
                    writeup_links.append(href)

        print(f"  Found {len(writeup_links)} potential writeup pages")

        for url in tqdm(writeup_links[:30]):
            try:
                r = requests.get(url, headers=HEADERS, timeout=15)
                soup = BeautifulSoup(r.content, 'html.parser')

                for tag in soup(['script', 'style', 'nav', 'footer']):
                    tag.decompose()

                title = soup.find('h1')
                title_text = title.get_text(strip=True) if title else 'HTB Writeup'

                main = soup.find('main') or soup.find('article')
                if main:
                    content = main.get_text(separator='\n', strip=True)

                    if len(content) > 500:
                        data.append({
                            'url': url,
                            'title': title_text,
                            'content': content[:15000],
                            'source': 'htb_rana_khalil',
                            'type': 'writeup',
                            'lang': 'en'
                        })

                time.sleep(1)

            except Exception as e:
                pass

        print(f"  ✅ Collected {len(data)} writeups")

    except Exception as e:
        print(f"  ❌ Error: {e}")

    return data


def fetch_tryhackme_writeups():
    """Fetch TryHackMe writeups from various sources"""
    print("\n[TryHackMe] Fetching writeups...")

    data = []

    # Popular THM writeup sources
    thm_sources = [
        'https://github.com/Sq00ky/TryHackMe-Rooms',
        'https://github.com/Kevinovitz/TryHackMe_Writeups',
    ]

    # We can also search for THM writeups on Medium
    try:
        search_url = 'https://medium.com/search?q=tryhackme%20writeup'
        r = requests.get(search_url, headers=HEADERS, timeout=15)

        # Medium has anti-scraping, so this is just a placeholder
        print("  ℹ️  Medium writeups require different approach (API or selenium)")

    except Exception as e:
        pass

    print(f"  ⚠️  TODO: Implement GitHub repo scraping for THM writeups")
    print(f"  Collected {len(data)} writeups")

    return data


def fetch_vulnhub_writeups():
    """Fetch VulnHub writeups"""
    print("\n[VulnHub] Fetching writeups...")

    data = []

    # VulnHub writeup sources
    sources = [
        'https://www.hackingarticles.in/category/vulnhub/',
    ]

    try:
        url = sources[0]
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.content, 'html.parser')

        # Find article links
        articles = soup.find_all('article')

        print(f"  Found {len(articles)} articles on page 1")

        for article in tqdm(articles[:20]):
            try:
                link = article.find('a', href=True)
                if not link:
                    continue

                article_url = link['href']

                r = requests.get(article_url, headers=HEADERS, timeout=15)
                soup = BeautifulSoup(r.content, 'html.parser')

                for tag in soup(['script', 'style', 'nav', 'footer', 'aside']):
                    tag.decompose()

                title = soup.find('h1')
                title_text = title.get_text(strip=True) if title else 'VulnHub Writeup'

                content_div = soup.find(class_='entry-content') or soup.find('article')
                if content_div:
                    content = content_div.get_text(separator='\n', strip=True)

                    if len(content) > 500:
                        data.append({
                            'url': article_url,
                            'title': title_text,
                            'content': content[:15000],
                            'source': 'vulnhub_hackingarticles',
                            'type': 'writeup',
                            'lang': 'en'
                        })

                time.sleep(1)

            except Exception as e:
                pass

        print(f"  ✅ Collected {len(data)} writeups")

    except Exception as e:
        print(f"  ❌ Error: {e}")

    return data


def fetch_ctf_writeups():
    """Fetch recent CTF writeups"""
    print("\n[CTF] Fetching writeups from CTFtime and other sources...")

    data = []

    # CTF writeup aggregators
    sources = [
        'https://ctftime.org/writeups',
        'https://github.com/ctfs',
    ]

    try:
        # CTFtime writeups page
        r = requests.get(sources[0], headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.content, 'html.parser')

        # Find writeup links (this will need adjustment)
        links = soup.find_all('a', href=re.compile(r'/writeup/'))

        print(f"  Found {len(links)} writeup links on CTFtime")

        # Note: CTFtime often links to external writeups
        # We'd need to follow those links

        print(f"  ⚠️  TODO: Implement full CTFtime scraping")
        print(f"  Collected {len(data)} writeups")

    except Exception as e:
        print(f"  ❌ Error: {e}")

    return data


def fetch_ippsec_transcripts():
    """Fetch transcripts/descriptions from IppSec videos"""
    print("\n[IppSec] Fetching video metadata...")

    data = []

    # IppSec has a search tool at ippsec.rocks
    try:
        url = 'https://ippsec.rocks/'
        r = requests.get(url, headers=HEADERS, timeout=15)

        print(f"  ℹ️  IppSec videos available at ippsec.rocks")
        print(f"  ⚠️  TODO: Implement video transcript extraction")

    except Exception as e:
        pass

    return data


def main():
    """Main writeup collection pipeline"""
    print("="*70)
    print("Writeup Collection: HTB, TryHackMe, VulnHub, CTFs")
    print("="*70)

    all_data = []

    # Collect from all sources
    all_data.extend(fetch_0xdf_writeups(limit=50))  # Increase limit
    all_data.extend(fetch_rana_khalil_writeups())
    all_data.extend(fetch_tryhackme_writeups())
    all_data.extend(fetch_vulnhub_writeups())
    all_data.extend(fetch_ctf_writeups())
    all_data.extend(fetch_ippsec_transcripts())

    # Save results
    output_file = OUT / 'writeups_collection.jsonl'

    print(f"\n📝 Saving {len(all_data)} writeups to {output_file}...")

    with open(output_file, 'w', encoding='utf-8') as f:
        for item in all_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

    print("\n" + "="*70)
    print(f"✅ DONE! Collected {len(all_data)} writeups")
    print("="*70)

    # Breakdown
    sources = {}
    for item in all_data:
        source = item.get('source', 'unknown')
        sources[source] = sources.get(source, 0) + 1

    print("\nBreakdown by source:")
    for source, count in sorted(sources.items()):
        print(f"  • {source}: {count} writeups")


if __name__ == '__main__':
    main()
