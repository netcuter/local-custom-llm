#!/usr/bin/env python3
"""
Web Scraper - pobiera artykuły ze stron internetowych
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Optional
import requests
from bs4 import BeautifulSoup
import hashlib

class WebScraper:
    def __init__(self, output_dir: str = "data/raw"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def scrape_article(self, url: str, category: str = "general") -> Dict:
        """Pobiera artykuł ze strony"""
        try:
            print(f"Pobieram: {url}")
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Wyciągnij tytuł
            title = soup.find('h1')
            title_text = title.get_text(strip=True) if title else soup.title.string if soup.title else "No title"

            # Wyciągnij treść główną
            # Usuń niepotrzebne elementy
            for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
                tag.decompose()

            # Szukaj głównej treści
            main_content = soup.find('article') or soup.find('main') or soup.find('div', class_=lambda x: x and 'content' in x.lower())

            if main_content:
                text = main_content.get_text(separator='\n', strip=True)
            else:
                text = soup.get_text(separator='\n', strip=True)

            # Oczyszczanie tekstu
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            text = '\n'.join(lines)

            # Generuj hash jako ID
            url_hash = hashlib.md5(url.encode()).hexdigest()[:12]

            result = {
                'url': url,
                'url_hash': url_hash,
                'category': category,
                'title': title_text,
                'content': text,
                'length': len(text),
            }

            # Zapisz
            output_file = self.output_dir / f"web_{url_hash}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)

            print(f"✓ Zapisano: {output_file} ({len(text)} znaków)")
            return result

        except Exception as e:
            print(f"Błąd scraping {url}: {e}")
            return {}

    def scrape_from_config(self, config_file: str):
        """Pobiera wszystkie artykuły z pliku konfiguracyjnego"""
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        articles = config.get('articles', {}).get('web', [])

        results = []
        for article_data in articles:
            if isinstance(article_data, dict):
                url = article_data.get('url')
                category = article_data.get('category', 'general')
                if url:
                    result = self.scrape_article(url, category)
                    if result:
                        results.append(result)

        return results

if __name__ == "__main__":
    scraper = WebScraper()

    # Scrape survival articles
    print("=== Scraping SURVIVAL articles ===")
    scraper.scrape_from_config("data/prompts/survival_sources.yaml")

    # Scrape coding articles
    print("\n=== Scraping CODING articles ===")
    scraper.scrape_from_config("data/prompts/coding_sources.yaml")

    print("\n✓ Web scraping ukończony!")
