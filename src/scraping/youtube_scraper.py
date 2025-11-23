#!/usr/bin/env python3
"""
YouTube Video Scraper - pobiera transkrypty z filmów YouTube
"""

import os
import json
import yaml
from pathlib import Path
from typing import List, Dict, Optional
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import yt_dlp
import re

class YouTubeScraper:
    def __init__(self, output_dir: str = "data/raw"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def extract_video_id(self, url: str) -> Optional[str]:
        """Wyciąga video ID z URL YouTube"""
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?]*)',
            r'youtube\.com\/embed\/([^&\n?]*)',
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    def get_transcript(self, video_id: str, languages: List[str] = ['pl', 'en']) -> Optional[str]:
        """Pobiera transkrypt filmu"""
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

            # Próbuj najpierw polskiego
            for lang in languages:
                try:
                    transcript = transcript_list.find_transcript([lang])
                    formatter = TextFormatter()
                    text = formatter.format_transcript(transcript.fetch())
                    return text
                except:
                    continue

            return None
        except Exception as e:
            print(f"Błąd pobierania transkryptu dla {video_id}: {e}")
            return None

    def get_metadata(self, url: str) -> Dict:
        """Pobiera metadata filmu"""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title'),
                    'description': info.get('description'),
                    'duration': info.get('duration'),
                    'upload_date': info.get('upload_date'),
                    'channel': info.get('channel'),
                    'view_count': info.get('view_count'),
                }
        except Exception as e:
            print(f"Błąd pobierania metadanych: {e}")
            return {}

    def scrape_video(self, url: str, category: str = "general") -> Dict:
        """Pobiera kompletne dane z filmu"""
        video_id = self.extract_video_id(url)
        if not video_id:
            print(f"Nie można wyciągnąć video ID z: {url}")
            return {}

        print(f"Pobieram dane dla: {video_id}")

        # Metadata
        metadata = self.get_metadata(url)

        # Transkrypt
        transcript = self.get_transcript(video_id)

        if not transcript:
            print(f"Brak transkryptu dla {video_id}")
            return {}

        result = {
            'video_id': video_id,
            'url': url,
            'category': category,
            'metadata': metadata,
            'transcript': transcript,
        }

        # Zapisz
        output_file = self.output_dir / f"youtube_{video_id}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"✓ Zapisano: {output_file}")
        return result

    def scrape_from_config(self, config_file: str):
        """Pobiera wszystkie filmy z pliku konfiguracyjnego"""
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        videos = config.get('videos', {}).get('youtube', [])

        results = []
        for video_data in videos:
            if isinstance(video_data, dict):
                url = video_data.get('url')
                category = video_data.get('category', 'general')
                if url:
                    result = self.scrape_video(url, category)
                    if result:
                        results.append(result)

        return results

if __name__ == "__main__":
    scraper = YouTubeScraper()

    # Scrape survival videos
    print("=== Scraping SURVIVAL videos ===")
    scraper.scrape_from_config("data/prompts/survival_sources.yaml")

    # Scrape coding videos
    print("\n=== Scraping CODING videos ===")
    scraper.scrape_from_config("data/prompts/coding_sources.yaml")

    print("\n✓ Scraping ukończony!")
