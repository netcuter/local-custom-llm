# 📋 PLANY ROZWOJU PROJEKTÓW GITHUB - netcuter

**Autor:** Seb (pentester@netcuter.com)  
**Data:** 2025-11-28  
**Cel:** Szczegółowe instrukcje dla prostszych modeli AI (Sonnet/Haiku)

---

## 🔥 PROJEKT 1: local-custom-llm (PRIORYTET)

**Ścieżka:** `/home/claude/Local-LLM-with-voice-support/`  
**Opis:** Dual-model chatbot z FastAPI backend + React frontend

### ✅ ZREALIZOWANE:
- [x] FastAPI backend z Uvicorn
- [x] Dual-model: Granite (agent) + Gemma (main)
- [x] 5 narzędzi: shell, web_search, files, weather, kiwix
- [x] XML tool calling format dla Granite
- [x] Failover między serwerami LM Studio
- [x] Dynamic IP detection (laptop priority)
- [x] Conversation compacting (redukcja tokenów ~65%)

### 📝 TODO - KRYTYCZNE (MUSI BYĆ):

#### TODO-1: Popraw obsługę błędów tool calling
```
PLIK: backend/main.py
LOKALIZACJA: Funkcja parse_tool_calls()
ZADANIE: 
1. Dodaj try-except wokół XML parsing
2. Jeśli parsing XML się nie powiedzie, spróbuj JSON
3. Jeśli żaden format nie działa, zwróć pustą listę (nie crash)
4. Loguj błędy do pliku debug.log

PRZYKŁAD KODU:
def parse_tool_calls(content: str) -> list:
    """Parse tool calls from model response - XML or JSON"""
    tools = []
    try:
        # Najpierw próbuj XML (Granite format)
        if "<tool_call>" in content:
            # ... XML parsing
            pass
        elif "tool_calls" in content or '"name"' in content:
            # Fallback do JSON
            # ... JSON parsing
            pass
    except Exception as e:
        logging.error(f"Tool parsing error: {e}")
        return []
    return tools
```

#### TODO-2: Dodaj timeout dla LM Studio requests
```
PLIK: backend/main.py
LOKALIZACJA: Wszystkie async with aiohttp.ClientSession() calls
ZADANIE:
1. Ustaw timeout na 120 sekund dla completion requests
2. Ustaw timeout na 5 sekund dla health checks
3. Dodaj retry logic (max 3 próby)

PRZYKŁAD:
timeout = aiohttp.ClientTimeout(total=120, connect=10)
async with aiohttp.ClientSession(timeout=timeout) as session:
    for attempt in range(3):
        try:
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    return await response.json()
        except asyncio.TimeoutError:
            logging.warning(f"Attempt {attempt+1} timeout")
            continue
    raise HTTPException(503, "LM Studio server timeout")
```

#### TODO-3: Ujednolic format odpowiedzi API
```
PLIK: backend/main.py
ZADANIE: Stwórz standard response format

STRUKTURA:
{
    "success": bool,
    "message": str,
    "data": {
        "response": str,          # Odpowiedź modelu
        "model_used": str,        # Który model odpowiedział
        "tools_called": list,     # Lista wywołanych narzędzi
        "tokens_used": int,       # Ilość tokenów
        "processing_time": float  # Czas w sekundach
    },
    "error": str | null
}
```

### 📝 TODO - WAŻNE (POWINNO BYĆ):

#### TODO-4: Health check endpoint
```
PLIK: backend/main.py
ENDPOINT: GET /api/health
ZADANIE: Zwróć status wszystkich komponentów

ODPOWIEDŹ:
{
    "status": "healthy" | "degraded" | "unhealthy",
    "components": {
        "backend": {"status": "up", "version": "1.0.0"},
        "agent_server": {"status": "up", "model": "granite-4h-tiny", "ip": "172.22.48.1:8087"},
        "main_server": {"status": "down", "model": "gemma-3-4b", "ip": "192.168.137.1:8087"},
        "kiwix": {"status": "up", "ip": "192.168.56.1:8008"}
    },
    "timestamp": "2025-11-28T12:00:00Z"
}
```

#### TODO-5: Lepsze logowanie
```
PLIK: backend/main.py (na początku)
ZADANIE: Skonfiguruj strukturalne logowanie

KONFIGURACJA:
import logging
import json
from datetime import datetime

# JSON formatter dla lepszej analizy
class JSONFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "line": record.lineno
        })

# Setup
handler = logging.FileHandler('/home/claude/Local-LLM-with-voice-support/backend/logs/app.log')
handler.setFormatter(JSONFormatter())
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.INFO)
```

#### TODO-6: Frontend - wskaźnik ładowania
```
PLIK: frontend/src/components/ChatWindow.jsx
ZADANIE: Dodaj animowany wskaźnik podczas oczekiwania na odpowiedź

KOMPONENTY DO DODANIA:
1. LoadingSpinner.jsx - animacja kółka
2. TypingIndicator.jsx - "..." pulsujące kropki
3. W ChatWindow - stan isLoading

PRZYKŁAD:
const [isLoading, setIsLoading] = useState(false);

// W handleSend:
setIsLoading(true);
try {
    const response = await fetch('/api/chat', ...);
    // ...
} finally {
    setIsLoading(false);
}

// W render:
{isLoading && <TypingIndicator />}
```

### 📝 TODO - OPCJONALNE (MIŁO MIEĆ):

#### TODO-7: Historia konwersacji w localStorage
```
PLIK: frontend/src/hooks/useConversationHistory.js (nowy plik)
ZADANIE: Zapisuj/wczytuj historię rozmów

FUNKCJE:
- saveConversation(id, messages) - zapisz do localStorage
- loadConversation(id) - wczytaj z localStorage
- listConversations() - lista wszystkich zapisanych
- deleteConversation(id) - usuń konwersację
- exportConversation(id, format) - eksport do JSON/MD
```

#### TODO-8: Ciemny motyw
```
PLIK: frontend/src/styles/themes.css (nowy plik)
ZADANIE: Dodaj przełącznik jasny/ciemny motyw

ZMIENNE CSS:
:root {
    --bg-primary: #ffffff;
    --bg-secondary: #f5f5f5;
    --text-primary: #333333;
    --accent: #4a90d9;
}

[data-theme="dark"] {
    --bg-primary: #1a1a2e;
    --bg-secondary: #16213e;
    --text-primary: #eaeaea;
    --accent: #e94560;
}
```

#### TODO-9: Eksport konwersacji
```
PLIK: backend/main.py
ENDPOINT: GET /api/export/{conversation_id}?format=md|json|pdf
ZADANIE: Eksportuj konwersację do różnych formatów

FORMATY:
- md: Markdown z formatowaniem
- json: Surowe dane
- pdf: Poprzez pandoc konwersja z MD
```

---

## 🔐 PROJEKT 2: Hexstrike-AI (Fork)

**Repozytorium:** https://github.com/netcuter/Hexstrike-AI  
**Opis:** Fork MCP server dla pentestingu z 150+ narzędziami

### 📝 TODO - DOSTOSOWANIA:

#### TODO-H1: Dodaj polskie komentarze
```
PLIKI: Wszystkie .py w głównym katalogu
ZADANIE: Dodaj polskie docstringi dla kluczowych funkcji
POWÓD: Łatwiejsza nawigacja i nauka
```

#### TODO-H2: Integracja z Twoim local-custom-llm
```
PLIK: Nowy plik: integrations/local_llm_bridge.py
ZADANIE: Stwórz bridge między Hexstrike a Twoim backendem

FUNKCJE:
- forward_to_local_llm(prompt) - przekieruj do lokalnego Granite
- get_tool_decision(context) - zapytaj Granite o wybór narzędzia
- execute_with_fallback(tool, params) - wykonaj z failover
```

#### TODO-H3: Filtruj niebezpieczne narzędzia
```
PLIK: config/tool_whitelist.yaml (nowy)
ZADANIE: Stwórz whitelist bezpiecznych narzędzi do nauki

ZAWARTOŚĆ:
safe_tools:
  - nmap_basic      # Tylko podstawowe skanowanie
  - whois_lookup
  - dns_enum
  - ssl_check
  - header_analysis
  
blocked_tools:      # NIE używać bez autoryzacji
  - sqlmap_full
  - exploit_*
  - brute_*
```

#### TODO-H4: Dodaj tryb "dry-run"
```
PLIK: hexstrike_mcp.py
ZADANIE: Dodaj flagę --dry-run która tylko pokazuje co by się wykonało

UŻYCIE:
python hexstrike_mcp.py --dry-run
# Zamiast wykonywać: "nmap -sV target.com"
# Pokaże: "[DRY-RUN] Would execute: nmap -sV target.com"
```

---

## 🔧 PROJEKT 3: system (bash scripts)

**Repozytorium:** https://github.com/netcuter/system  
**Opis:** Kolekcja skryptów bash/Python do administracji systemem

### 📝 TODO - ROZBUDOWA:

#### TODO-S1: Struktura katalogów
```
ZADANIE: Zreorganizuj repozytorium

NOWA STRUKTURA:
system/
├── README.md
├── install.sh              # Instalator wszystkich skryptów
├── network/
│   ├── ip_scanner.sh
│   ├── port_monitor.sh
│   └── wifi_analyzer.py
├── security/
│   ├── log_analyzer.sh
│   ├── firewall_rules.sh
│   └── ssh_hardening.sh
├── backup/
│   ├── rsync_backup.sh
│   └── db_backup.py
├── monitoring/
│   ├── system_health.sh
│   ├── disk_alert.sh
│   └── process_monitor.py
└── utils/
    ├── cleanup.sh
    └── update_all.sh
```

#### TODO-S2: Skrypt monitoringu dla LM Studio
```
PLIK: monitoring/lmstudio_health.sh
ZADANIE: Monitoruj serwery LM Studio

FUNKCJE:
- Sprawdź czy serwer odpowiada
- Sprawdź użycie GPU/RAM
- Wyślij alert jeśli serwer nie odpowiada
- Loguj do syslog

UŻYCIE:
./lmstudio_health.sh --servers "172.22.48.1:8087,192.168.137.1:8087"
```

#### TODO-S3: Automatyczne backupy konfiguracji
```
PLIK: backup/config_backup.sh
ZADANIE: Backup ważnych konfiguracji

CO BACKUPOWAĆ:
- ~/.lmstudio/
- /home/claude/Local-LLM-with-voice-support/backend/config/
- ~/.config/claude/
- /etc/nginx/ (jeśli używasz)

GDZIE:
- Lokalnie: /backup/configs/YYYY-MM-DD/
- Opcjonalnie: Google Drive via rclone
```

---

## 🌐 PROJEKT 4: network (C++ sieciowe)

**Repozytorium:** https://github.com/netcuter/network  
**Opis:** Narzędzia sieciowe w C++

### 📝 TODO - MODERNIZACJA:

#### TODO-N1: Aktualizacja do C++17/20
```
ZADANIE: Zmodernizuj kod do nowszego standardu C++

ZMIANY:
- Użyj std::optional zamiast nullptr checks
- Użyj std::filesystem zamiast POSIX calls
- Użyj structured bindings gdzie możliwe
- Dodaj CMakeLists.txt
```

#### TODO-N2: Dodaj testy jednostkowe
```
PLIK: tests/CMakeLists.txt + tests/*.cpp
FRAMEWORK: Google Test lub Catch2

TESTY:
- test_packet_parser.cpp
- test_socket_utils.cpp
- test_protocol_handlers.cpp
```

---

## 🔑 PROJEKT 5: autojwt (Shell)

**Repozytorium:** https://github.com/netcuter/autojwt  
**Opis:** Narzędzia do testowania JWT

### 📝 TODO - ROZSZERZENIA:

#### TODO-J1: Dodaj więcej ataków
```
PLIK: attacks/
NOWE ATAKI:
- none_algorithm.sh      # Atak "alg: none"
- key_confusion.sh       # RS256 -> HS256 confusion
- kid_injection.sh       # SQL injection przez kid
- jwk_injection.sh       # Embedded JWK attack
```

#### TODO-J2: Integracja z Burp Suite
```
PLIK: burp_integration/
ZADANIE: Stwórz extension do Burp Suite

FUNKCJE:
- Automatyczne wykrywanie JWT w requests/responses
- Podświetlanie payload
- Quick decode/encode
- Test common vulnerabilities
```

#### TODO-J3: Raportowanie
```
PLIK: report_generator.sh
ZADANIE: Generuj raporty z testów JWT

FORMAT:
- HTML z kolorowymi wynikami
- JSON dla automatyzacji
- Markdown dla dokumentacji
```

---

## 🎯 PRIORYTETYZACJA DLA AI:

### 🔴 KRYTYCZNE (zrób najpierw):
1. TODO-1: Obsługa błędów tool calling
2. TODO-2: Timeout dla requests
3. TODO-4: Health check endpoint

### 🟡 WAŻNE (potem):
4. TODO-3: Ujednolicony format API
5. TODO-5: Lepsze logowanie
6. TODO-6: Loading indicator w frontend

### 🟢 OPCJONALNE (jak będzie czas):
7. TODO-7: Historia w localStorage
8. TODO-8: Ciemny motyw
9. TODO-H2: Integracja Hexstrike

---

## 📌 INSTRUKCJE DLA MODELI AI:

**Gdy pracujesz nad tymi zadaniami:**

1. **ZAWSZE** przeczytaj istniejący kod przed modyfikacją
2. **NIGDY** nie usuwaj działającego kodu bez backup
3. **TESTUJ** każdą zmianę przed commitem
4. **KOMENTUJ** po polsku lub angielsku (preferencja: polski)
5. **LOGUJ** wszystkie błędy i ważne operacje

**Format commit message:**
```
[PROJEKT] TODO-X: Krótki opis

Szczegóły co zostało zrobione.
Jeśli są breaking changes - opisz.

Testowano na: [środowisko]
```

**Przykład:**
```
[local-custom-llm] TODO-1: Poprawiona obsługa błędów tool calling

- Dodano try-except w parse_tool_calls()
- Fallback z XML do JSON
- Logowanie błędów do debug.log

Testowano na: Ubuntu 22.04, Python 3.11
```

---

✝️ CHWAŁA BOGU ZA KAŻDY POSTĘP! 🙏
ALLELUJA!
