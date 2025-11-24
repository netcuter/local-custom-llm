#!/usr/bin/env python3
"""
Collect writeups directly from GitHub repositories
"""

import json
import subprocess
from pathlib import Path
from tqdm import tqdm
import re

OUT = Path('data/raw')
OUT.mkdir(parents=True, exist_ok=True)

REPOS_DIR = Path('data/repos')
REPOS_DIR.mkdir(parents=True, exist_ok=True)

# GitHub repositories with writeups
GITHUB_REPOS = [
    # HTB writeups
    ('Hackplayers/hackthebox-writeups', 'htb'),
    ('xct/xct.github.io', 'htb_xct'),

    # TryHackMe writeups
    ('Kevinovitz/TryHackMe_Writeups', 'thm'),

    # CTF writeups
    ('ctfs/write-ups-2024', 'ctf_2024'),
    ('ctfs/write-ups-2023', 'ctf_2023'),

    # VulnHub
    ('Ignitetechnologies/Vulnhub-CTF-Writeups', 'vulnhub'),
]


def clone_or_update_repo(repo_name):
    """Clone repository or update if exists"""
    repo_path = REPOS_DIR / repo_name.split('/')[-1]

    if repo_path.exists():
        print(f"  ✓ Repo exists: {repo_name}")
        return repo_path

    try:
        print(f"  📥 Cloning {repo_name}...")
        subprocess.run(
            ['git', 'clone', '--depth', '1',
             f'https://github.com/{repo_name}.git',
             str(repo_path)],
            check=True,
            capture_output=True,
            timeout=60
        )
        return repo_path
    except Exception as e:
        print(f"  ❌ Failed to clone {repo_name}: {e}")
        return None


def extract_writeups_from_repo(repo_path, source_tag):
    """Extract writeup content from markdown files"""
    data = []

    if not repo_path or not repo_path.exists():
        return data

    # Find all markdown files
    md_files = list(repo_path.rglob('*.md'))

    # Filter out README, LICENSE, etc.
    md_files = [f for f in md_files if not any(
        skip in f.name.lower()
        for skip in ['readme', 'license', 'contributing', 'changelog']
    )]

    print(f"  📖 Processing {len(md_files)} markdown files...")

    for md_file in tqdm(md_files):
        try:
            with open(md_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Skip if too short
            if len(content) < 500:
                continue

            # Get title from first heading or filename
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            title = title_match.group(1) if title_match else md_file.stem

            # Create GitHub URL
            rel_path = md_file.relative_to(repo_path)
            github_url = f'https://github.com/{repo_path.name}/blob/master/{rel_path}'

            data.append({
                'url': github_url,
                'title': title,
                'content': content[:20000],  # Limit to 20k chars
                'source': source_tag,
                'type': 'writeup',
                'lang': 'en'
            })

        except Exception as e:
            pass

    return data


def main():
    """Main GitHub writeup collection"""
    print("="*70)
    print("GitHub Writeup Collection")
    print("="*70)

    all_data = []

    for repo_name, source_tag in GITHUB_REPOS:
        print(f"\n[{source_tag}] Processing {repo_name}")

        # Clone/update repo
        repo_path = clone_or_update_repo(repo_name)

        if repo_path:
            # Extract writeups
            writeups = extract_writeups_from_repo(repo_path, source_tag)
            all_data.extend(writeups)
            print(f"  ✅ Extracted {len(writeups)} writeups")

    # Save results
    output_file = OUT / 'github_writeups.jsonl'

    print(f"\n📝 Saving {len(all_data)} writeups to {output_file}...")

    with open(output_file, 'w', encoding='utf-8') as f:
        for item in all_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

    print("\n" + "="*70)
    print(f"✅ DONE! Collected {len(all_data)} writeups from GitHub")
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
