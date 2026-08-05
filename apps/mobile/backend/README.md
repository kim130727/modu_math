# Modu Math Backend

Minimal Django REST Framework backend for the Flutter MVP.

Current scope:

- Anonymous student session
- Learning attempt recording
- Daily summary, unit mastery, review queue reads
- Tutor proxy endpoint with deterministic scaffold responses

The tutor endpoint is intentionally a proxy boundary. OpenAI or other provider
keys must live only in backend environment variables when a real provider adapter
is added.

## Setup

```powershell
python -m pip install -r backend\requirements.txt
python backend\manage.py test api
python backend\manage.py runserver 127.0.0.1:8000
```

Flutter can use this server with:

```dotenv
AI_TUTOR_MODE=backend
BACKEND_API_BASE_URL=http://127.0.0.1:8000
BACKEND_SESSION_TOKEN=<token from /api/v1/auth/anonymous-session>
```

The in-memory store is for contract testing only. Replace it with PostgreSQL
models before production or multi-device sync work.
