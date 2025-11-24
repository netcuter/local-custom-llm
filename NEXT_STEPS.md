# Next Steps ✅

## ✅ Faza 1: Dane - GOTOWE
- ✅ 307 przykładów treningowych
- ✅ Writeups: HTB (196 total)
- ✅ Techniki: PortSwigger, PayloadsAllTheThings
- ✅ Skrypty do zbierania danych

## ✅ Faza 2: Trening - GOTOWE
- ✅ Skrypt treningowy `scripts/train.py`
- ✅ Skrypt testowy `scripts/inference.py`
- ✅ Dokumentacja `docs/TRAINING_GUIDE.md`
- ✅ Konfiguracja LoRA/QLoRA

## 🎯 Faza 3: Uruchomienie treningu
```bash
# 1. Instalacja zależności
pip install -r requirements.txt

# 2. Trening (8-12h na CPU, 2-3h na GPU)
python scripts/train.py

# 3. Test modelu
python scripts/inference.py --mode interactive
```

## Konfiguracja treningu
- **Model**: IBM Granite 3.0 2B Instruct
- **Metoda**: LoRA (rank=16, alpha=32)
- **Kwantyzacja**: 4-bit (QLoRA)
- **Epochs**: 3
- **Batch size**: 1 + gradient accumulation (8)
- **Learning rate**: 2e-4
- **Max seq length**: 2048

## 🎯 Faza 4: Opcjonalnie
- [ ] Export do GGUF dla llama.cpp
- [ ] Deploy jako API (FastAPI)
- [ ] Web interface
- [ ] Dodaj więcej danych (najnowsze CVEs 2024-2025)
- [ ] Douczenie polskiego (jeśli potrzebne)
