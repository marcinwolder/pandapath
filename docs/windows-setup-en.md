# Windows Instructions (English)

## Requirements

- Windows 10/11 with virtualization enabled, WSL2 + Docker Desktop.

## Backend + llama via Docker (recommended)

1) Clone and copy env:

   ```powershell
   git clone <repo> pandapath
   cd pandapath
   copy apps\backend\.env.example apps\backend\.env
   ```

2) Fill in `apps\backend\.env` (Google Places API key).
3) Run:

   ```powershell
   docker compose up --build
   ```

4) Expected:
   - Backend: <http://localhost:5000>
   - Llama: <http://localhost:3000> (first run downloads ~600MB into `apps/llama/models`)

## Native backend without Docker

Use only when Docker is unavailable; the llama model must be remote/on another host.

```powershell
cd apps\backend
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m src.backend.main --no_db
```
