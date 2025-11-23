#!/usr/bin/env python3
"""
Claude Distillation - generuje training examples używając Claude
"""

import json
import yaml
from pathlib import Path
from typing import List, Dict
import time

class ClaudeDistiller:
    """
    Distillacja wiedzy z użyciem Claude.

    UWAGA: Ten skrypt będzie wykonywany w środowisku Claude Code,
    więc używamy interakcji z użytkownikiem zamiast API.
    """

    def __init__(self, output_dir: str = "data/generated"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_topics(self, config_file: str) -> Dict:
        """Ładuje listę tematów z pliku YAML"""
        with open(config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def generate_prompt_for_topic(self, category: str, topic: str, count: int = 5) -> str:
        """Generuje prompt dla danego tematu"""

        if "survival" in category.lower():
            system = """Jesteś ekspertem od survivalu, bushcraftu i ratownictwa z wieloletnim doświadczeniem praktycznym.
Twoja wiedza jest praktyczna, sprawdzona i bezpieczna."""

            prompt = f"""Wygeneruj {count} różnych par pytanie-odpowiedź na temat: {topic} w kontekście survivalu.

Wymagania:
- Pytania powinny być różnorodne (od podstawowych do zaawansowanych)
- Odpowiedzi szczegółowe, praktyczne i bezpieczne
- Uwzględnij aspekty praktyczne, nie tylko teorię
- Dodaj wskazówki bezpieczeństwa gdzie to konieczne

Format JSON (bez markdown, sam JSON):
[
  {{
    "question": "Pytanie w języku polskim",
    "answer": "Szczegółowa odpowiedź w języku polskim",
    "difficulty": "basic|intermediate|advanced",
    "safety_notes": "Opcjonalne uwagi bezpieczeństwa"
  }}
]"""

        elif "coding" in category.lower() or "hacking" in category.lower():
            system = """Jesteś ekspertem cybersecurity i programowania.
Wszystkie przykłady dotyczące hackingu odnoszą się TYLKO do authorized/ethical pentestingu."""

            prompt = f"""Wygeneruj {count} różnych przykładów na temat: {topic}.

Wymagania:
- Dla kodu: podaj przykłady działającego kodu z wyjaśnieniami
- Dla hackingu: TYLKO ethical/authorized scenariusze
- Wyjaśnij nie tylko "jak" ale i "dlaczego"
- Uwzględnij best practices i zabezpieczenia

Format JSON (bez markdown, sam JSON):
[
  {{
    "question": "Pytanie lub zadanie",
    "context": "Opcjonalny kontekst",
    "answer": "Szczegółowa odpowiedź z kodem/przykładami",
    "code": "Przykładowy kod jeśli applicable",
    "security_note": "Uwagi o bezpieczeństwie"
  }}
]"""

        else:
            prompt = f"Wygeneruj {count} par Q&A o temacie: {topic}"

        return prompt

    def save_examples(self, examples: List[Dict], category: str, topic: str):
        """Zapisuje wygenerowane przykłady"""
        timestamp = int(time.time())
        filename = f"{category}_{topic}_{timestamp}.jsonl"
        output_file = self.output_dir / filename

        with open(output_file, 'w', encoding='utf-8') as f:
            for example in examples:
                f.write(json.dumps(example, ensure_ascii=False) + '\n')

        print(f"✓ Zapisano {len(examples)} przykładów: {output_file}")

    def generate_instruction_format(self, raw_example: Dict, category: str) -> Dict:
        """Konwertuje surowy przykład do formatu instruction-tuning"""

        if "survival" in category.lower():
            return {
                "instruction": raw_example.get("question", ""),
                "input": "",
                "output": raw_example.get("answer", ""),
                "metadata": {
                    "category": category,
                    "difficulty": raw_example.get("difficulty", "intermediate"),
                    "safety_notes": raw_example.get("safety_notes", ""),
                    "source": "claude_distillation"
                }
            }
        else:
            return {
                "instruction": raw_example.get("question", ""),
                "input": raw_example.get("context", ""),
                "output": raw_example.get("answer", ""),
                "metadata": {
                    "category": category,
                    "code": raw_example.get("code", ""),
                    "security_note": raw_example.get("security_note", ""),
                    "source": "claude_distillation"
                }
            }

def main():
    """
    Główna funkcja - generuje prompty do użytkownika
    """
    print("""
╔══════════════════════════════════════════════════════════════╗
║         CLAUDE DISTILLATION - Generowanie Danych             ║
╚══════════════════════════════════════════════════════════════╝

Ten skrypt generuje prompty, które będą użyte do destylacji wiedzy.

Użytkownik Claude Code może:
1. Skopiować prompty i poprosić Claude o wygenerowanie danych
2. Wkleić odpowiedzi Claude do plików
3. Lub uruchomić interaktywnie

""")

    distiller = ClaudeDistiller()

    # Przykład dla SURVIVAL
    config = distiller.load_topics("data/prompts/survival_sources.yaml")
    topics = config.get('topics', {})

    print("\n=== PRZYKŁADOWE PROMPTY - SURVIVAL ===\n")

    for category, topic_list in list(topics.items())[:2]:  # Pierwsze 2 kategorie
        for topic in topic_list[:2]:  # Pierwsze 2 tematy
            prompt = distiller.generate_prompt_for_topic(f"survival_{category}", topic, count=3)
            print(f"\n{'='*60}")
            print(f"KATEGORIA: {category}")
            print(f"TEMAT: {topic}")
            print(f"{'='*60}")
            print(prompt)
            print("\n")

if __name__ == "__main__":
    main()
