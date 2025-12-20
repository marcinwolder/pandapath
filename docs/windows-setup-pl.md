# Instrukcja Windows (Polski)

## Wymagania

- Windows 10/11 z włączoną wirtualizacją, WSL2 + Docker Desktop.

## Backend + llama przez Docker (zalecane)

1) Klonowanie i kopia env:

   ```powershell
   git clone <repo> pandapath
   cd pandapath
   copy apps\backend\.env.example apps\backend\.env
   ```

2) Uzupełnij `apps\backend\.env` (klucz Google Places API).
3) Uruchom:

   ```powershell
   docker compose up --build
   ```

4) Oczekiwane:
   - Backend: <http://localhost:5000>
   - Llama: <http://localhost:3000> (pierwsze uruchomienie pobiera ~600MB do `apps/llama/models`)

## Natywny backend bez Dockera

Używaj tylko gdy Docker niedostępny; model llama musi być zdalny/inny host.

```powershell
cd apps\backend
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python -m src.backend.main --no_db
```
