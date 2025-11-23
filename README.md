# Local Custom LLM - Fine-tuning Project

## 🎯 Cel Projektu

Fine-tuning modeli LLM (Bielik 4B) do specjalistycznych zastosowań:
- **Survival Model** - wiedza o survivallu, bushcraft, pierwsza pomoc
- **Coding/Hacking Model** - programowanie, cybersecurity, ethical hacking

## 🏗️ Struktura Projektu

```
local-custom-llm/
├── data/                      # Dane treningowe
│   ├── prompts/              # Tematy i prompty do generowania
│   ├── raw/                  # Surowe dane (scraping)
│   ├── generated/            # Wygenerowane przez Claude
│   ├── curated/              # Przejrzane i poprawione
│   └── training/             # Finalne datasety
│       ├── survival/
│       └── coding-hacking/
│
├── src/                      # Kod źródłowy
│   ├── scraping/            # Web scraping
│   ├── distillation/        # Claude destylacja
│   ├── training/            # Fine-tuning pipeline
│   ├── evaluation/          # Testy i ewaluacja
│   └── export/              # Export do LM Studio (GGUF)
│
├── models/                   # Modele
│   ├── base/                # Model bazowy (Bielik 4B)
│   ├── survival/            # Wytrenowany survival
│   └── coding-hacking/      # Wytrenowany coding
│
├── configs/                  # Konfiguracje
├── scripts/                  # Utility scripts
└── notebooks/                # Jupyter notebooks
```

## 🚀 Pipeline

### Faza 1: Generowanie Danych (Claude Code - dzisiaj)
1. Web scraping + analiza filmów/artykułów
2. Claude destylacja (generowanie Q&A)
3. Walidacja i formatowanie
4. Commit do GitHub

### Faza 2: Fine-tuning (Lokalny PC - jutro+)
1. QLoRA fine-tuning (CPU optimized)
2. Monitoring i checkpoints
3. Export do GGUF (LM Studio)
4. Testy i ewaluacja

## 📊 Model Bazowy

**Bielik 4B** (polski LLM)
- Rozmiar: 4B parametrów
- Język: Polski
- Fine-tuning: QLoRA (CPU-friendly)

## ⚙️ Stack Technologiczny

- Python 3.10+
- PyTorch (CPU)
- Transformers (HuggingFace)
- PEFT (QLoRA)
- yt-dlp (YouTube transcripts)
- beautifulsoup4 (web scraping)

## 📝 Status

- [x] Struktura projektu
- [ ] Setup dependencies
- [ ] Survival dataset generation
- [ ] Fine-tuning pipeline
- [ ] Export do LM Studio

## 🎓 Modele Docelowe

1. **Survival Model** (FIRST) - w trakcie
2. **Coding/Hacking Model** - planned

---
**Created**: 2025-11-23
**Base Model**: Bielik 4B
**Method**: QLoRA Fine-tuning + Claude Distillation
