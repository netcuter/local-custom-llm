# Next Steps

## Strategia
1. **Faza 1**: Granite fine-tune na EN pentesting (OWASP, PortSwigger)
2. **Faza 2**: Później douczenie polskiego (opcjonalnie)

## Dane gotowe
- `data/raw/pentesting_data.jsonl` - 3 EN artykuły (OWASP)

## Potrzeba więcej
- Użyj HuggingFace datasets z `pentesting_sources.yaml`
- Albo scrape więcej OWASP/PortSwigger stron

## Training
```bash
# Lokalnie:
git clone repo
pip install -r requirements.txt
python scripts/train.py  # TODO: stworzyć
```
