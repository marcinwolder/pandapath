# Instrukcje dla Windows (polski)

## Wymagania

- Windows: Windows 10/11 z włączoną wirtualizacją, WSL2 i Docker Desktop (dla pracy z Dockerem).
- macOS: macOS 12+ (Intel lub Apple Silicon) z włączoną wirtualizacją i Docker Desktop (albo innym silnikiem Docker z `docker compose`).

## Backend + llama przez Docker (zalecane)

1) Sklonuj repo i skopiuj plik env:

   ```powershell
   # Windows PowerShell
   git clone <repo> pandapath
   cd pandapath
   copy apps\backend\.env.example apps\backend\.env
   ```

   ```bash
   # macOS / zsh lub bash
   git clone <repo> pandapath
   cd pandapath
   cp apps/backend/.env.example apps/backend/.env
   ```

2) Uzupełnij `apps\backend\.env` (klucz Google Places API).
3) Uruchom:

   ```powershell
   # Windows PowerShell
   docker compose up --build
   ```

   ```bash
   # macOS / zsh lub bash
   docker compose up --build
   ```

4) Oczekiwane:
   - Backend: <http://localhost:5000>
   - Llama: <http://localhost:3000> (przy pierwszym uruchomieniu pobiera ~600MB do `apps/llama/models`)

## Backend natywnie bez Dockera

Używaj tylko, gdy Docker jest niedostępny; model llama musi wtedy działać zdalnie/na innym hoście.

```powershell
# Windows PowerShell
cd apps\backend
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m src.backend.main --no_db
```

```bash
# macOS / zsh lub bash
cd apps/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.backend.main --no_db
```

## Llama bez Dockera (Windows i macOS)

Uruchom lokalnie serwer llama.cpp, jeśli nie możesz użyć Dockera. Korzysta z tego samego modelu TinyLlama i nasłuchuje na porcie 3000.

### Wymagania wstępne

- Python 3.10+ i `pip` dostępne w Twojej powłoce.
- Narzędzia build: Windows potrzebuje narzędzi C++ z Visual Studio (lub Build Tools for VS) oraz CMake; macOS potrzebuje Xcode Command Line Tools i `cmake` z Homebrew (`brew install cmake`).
- ~600MB wolnego miejsca na dysku na pobranie modelu do `apps/llama/models/`.

### Instalacja zależności

```powershell
# Windows PowerShell
cd apps\llama
py -m venv .venv
.venv\Scripts\activate
pip install --upgrade pip cmake
pip install "llama-cpp-python[server]==0.3.16"
```

```bash
# macOS / zsh lub bash
cd apps/llama
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip cmake
pip install "llama-cpp-python[server]==0.3.16"
```

### Pobierz model TinyLlama

```powershell
# Windows PowerShell
Invoke-WebRequest "https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_0.gguf" `
  -OutFile "apps/llama/models/tinyllama-1.1b-chat-v1.0.Q4_0.gguf"
```

```bash
# macOS / zsh lub bash
curl -L "https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_0.gguf" \
  -o apps/llama/models/tinyllama-1.1b-chat-v1.0.Q4_0.gguf
```

### Uruchom serwer

```powershell
# Windows PowerShell (z katalogu głównego repo lub apps\llama)
cd apps\llama
.venv\Scripts\activate
python -m llama_cpp.server --model "apps/llama/models/tinyllama-1.1b-chat-v1.0.Q4_0.gguf" --host 0.0.0.0 --port 3000
```

```bash
# macOS / zsh lub bash (z katalogu głównego repo lub apps/llama)
cd apps/llama
source .venv/bin/activate
python -m llama_cpp.server --model "apps/llama/models/tinyllama-1.1b-chat-v1.0.Q4_0.gguf" --host 0.0.0.0 --port 3000
```
