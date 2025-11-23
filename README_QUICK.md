# Quick Start - Polski Pentesting Model

## Status
- ✅ Projekt setup
- ✅ Scraping script gotowy
- ⚠️ Potrzebuję więcej danych

## Co masz
- `scripts/collect_data.py` - scraper
- `data/raw/pentesting_data.jsonl` - 2 EN artykuły

## Co zrobić dalej

### 1. Dodaj polskie linki
Edytuj `scripts/collect_data.py`:
```python
PL_SOURCES = [
    'https://zaufanatrzeciastrona.pl/KONKRETNY-ARTYKUL',
    'https://sekurak.pl/KONKRETNY-ARTYKUL',
    # dodaj więcej
]
```

### 2. Uruchom scraping
```bash
python3 scripts/collect_data.py
```

### 3. Fine-tuning (lokalnie)
```bash
# Będzie w kolejnym commicie
python3 scripts/train.py
```

## Model
- Base: Granite 4H Tiny MoE (7B, 1B aktywne)
- Target: Polski + Pentesting
- Training: 8-12h na CPU
