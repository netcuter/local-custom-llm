#!/usr/bin/env python3
"""
Advanced data collection for pentesting LLM fine-tuning
Sources:
1. HuggingFace datasets
2. PortSwigger Research (advanced techniques)
3. HackTheBox writeups
4. PayloadsAllTheThings (GitHub)
"""

import json
import time
from pathlib import Path
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import subprocess
import re

# Output directory
OUT = Path('data/raw')
OUT.mkdir(parents=True, exist_ok=True)

# User agent for requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}


# ===== 1. HuggingFace Datasets =====
def fetch_huggingface_datasets():
    """Fetch pentesting datasets from HuggingFace"""
    print("\n[1/4] Fetching HuggingFace datasets...")

    try:
        from datasets import load_dataset

        datasets_to_fetch = [
            # Add dataset names here when found
            # 'username/pentesting-dataset',
        ]

        all_data = []

        # For now, we'll add this as a TODO since we need to find actual datasets
        print("  ⚠️  TODO: Find and add pentesting datasets from HuggingFace")
        print("  Searching for: cybersecurity, pentesting, OWASP datasets")

        return all_data

    except Exception as e:
        print(f"  ❌ Error: {e}")
        return []


# ===== 2. PortSwigger Research =====
def fetch_portswigger_research():
    """Scrape PortSwigger Research articles (advanced techniques)"""
    print("\n[2/4] Scraping PortSwigger Research...")

    research_urls = [
        # Latest research and advanced techniques
        'https://portswigger.net/research',
        'https://portswigger.net/web-security/csrf',
        'https://portswigger.net/web-security/cors',
        'https://portswigger.net/web-security/xxe',
        'https://portswigger.net/web-security/ssrf',
        'https://portswigger.net/web-security/xss',
        'https://portswigger.net/web-security/sql-injection',
        'https://portswigger.net/web-security/deserialization',
        'https://portswigger.net/web-security/os-command-injection',
        'https://portswigger.net/web-security/authentication',
        'https://portswigger.net/web-security/access-control',
    ]

    data = []

    for url in tqdm(research_urls):
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(r.content, 'html.parser')

            # Remove unwanted elements
            for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
                tag.decompose()

            # Get title
            title = soup.find('h1')
            title_text = title.get_text(strip=True) if title else 'No title'

            # Get main content
            main = soup.find('main') or soup.find('article') or soup.find(class_='content')
            if main:
                content = main.get_text(separator='\n', strip=True)

                if len(content) > 200:  # Only if substantial content
                    data.append({
                        'url': url,
                        'title': title_text,
                        'content': content[:8000],  # Limit to 8k chars
                        'source': 'portswigger',
                        'lang': 'en'
                    })

            time.sleep(1)  # Be nice to the server

        except Exception as e:
            print(f"  ⚠️  Error {url}: {e}")

    print(f"  ✅ Fetched {len(data)} PortSwigger articles")
    return data


# ===== 3. HackTheBox Writeups =====
def fetch_htb_writeups():
    """Fetch HTB writeups from public sources"""
    print("\n[3/4] Fetching HTB writeups...")

    # Public HTB writeup sources
    writeup_sources = [
        'https://0xdf.gitlab.io/',  # Popular HTB writeups
        # Add more HTB writeup blogs
    ]

    data = []

    print("  ℹ️  Fetching from 0xdf.gitlab.io (comprehensive HTB writeups)...")

    try:
        # Fetch the main page to get list of writeups
        r = requests.get(writeup_sources[0], headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.content, 'html.parser')

        # Find writeup links (this will need adjustment based on site structure)
        links = soup.find_all('a', href=re.compile(r'/\d{4}/\d{2}/\d{2}/htb-'))

        print(f"  Found {len(links)} potential writeup links")

        # Limit to recent writeups (last 20)
        for link in links[:20]:
            try:
                url = link.get('href')
                if not url.startswith('http'):
                    url = 'https://0xdf.gitlab.io' + url

                r = requests.get(url, headers=HEADERS, timeout=15)
                soup = BeautifulSoup(r.content, 'html.parser')

                title = soup.find('h1')
                title_text = title.get_text(strip=True) if title else 'HTB Writeup'

                article = soup.find('article') or soup.find(class_='post-content')
                if article:
                    content = article.get_text(separator='\n', strip=True)

                    if len(content) > 500:
                        data.append({
                            'url': url,
                            'title': title_text,
                            'content': content[:10000],  # Limit to 10k chars
                            'source': 'htb_writeup',
                            'lang': 'en'
                        })

                time.sleep(2)  # Be respectful

            except Exception as e:
                print(f"  ⚠️  Error fetching writeup: {e}")

    except Exception as e:
        print(f"  ❌ Error: {e}")

    print(f"  ✅ Fetched {len(data)} HTB writeups")
    return data


# ===== 4. PayloadsAllTheThings =====
def fetch_payloadsallthethings():
    """Clone and process PayloadsAllTheThings repository"""
    print("\n[4/4] Processing PayloadsAllTheThings...")

    repo_url = 'https://github.com/swisskyrepo/PayloadsAllTheThings.git'
    repo_path = Path('data/repos/PayloadsAllTheThings')

    data = []

    try:
        # Clone repo if not exists
        if not repo_path.exists():
            print("  📥 Cloning repository...")
            repo_path.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(
                ['git', 'clone', '--depth', '1', repo_url, str(repo_path)],
                check=True,
                capture_output=True
            )
        else:
            print("  ✅ Repository already exists")

        # Process markdown files
        print("  📖 Processing markdown files...")
        md_files = list(repo_path.rglob('*.md'))

        for md_file in tqdm(md_files[:100]):  # Limit to first 100 files
            try:
                with open(md_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # Get title from first heading or filename
                title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                title = title_match.group(1) if title_match else md_file.stem

                # Skip if too short
                if len(content) < 200:
                    continue

                data.append({
                    'url': f'https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/{md_file.relative_to(repo_path)}',
                    'title': title,
                    'content': content[:15000],  # Limit to 15k chars
                    'source': 'payloadsallthethings',
                    'lang': 'en'
                })

            except Exception as e:
                pass  # Skip problematic files

        print(f"  ✅ Processed {len(data)} files from PayloadsAllTheThings")

    except Exception as e:
        print(f"  ❌ Error: {e}")

    return data


# ===== Main =====
def main():
    """Main data collection pipeline"""
    print("="*60)
    print("Advanced Pentesting Data Collection")
    print("="*60)

    all_data = []

    # Fetch from all sources
    all_data.extend(fetch_huggingface_datasets())
    all_data.extend(fetch_portswigger_research())
    all_data.extend(fetch_htb_writeups())
    all_data.extend(fetch_payloadsallthethings())

    # Save to JSONL
    output_file = OUT / 'pentesting_data_advanced.jsonl'

    print(f"\n📝 Saving {len(all_data)} records to {output_file}...")

    with open(output_file, 'w', encoding='utf-8') as f:
        for item in all_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

    print("\n" + "="*60)
    print(f"✅ DONE! Collected {len(all_data)} training examples")
    print("="*60)

    # Show breakdown
    sources = {}
    for item in all_data:
        source = item.get('source', 'unknown')
        sources[source] = sources.get(source, 0) + 1

    print("\nBreakdown by source:")
    for source, count in sources.items():
        print(f"  • {source}: {count} examples")


if __name__ == '__main__':
    main()
