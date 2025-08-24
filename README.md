# Backend + Widget Chat IA — Innerskin

## 1) Lancer en local
```bash
python -m venv .venv && . .venv/Scripts/activate        # Windows
# macOS/Linux: python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
set OPENAI_API_KEY=sk-...                                # Windows
# macOS/Linux: export OPENAI_API_KEY="sk-..."
uvicorn main:app --reload --port 8000
```

## 2) Déploiement Render
- Build: `pip install -r requirements.txt`
- Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Var d'env obligatoire: `OPENAI_API_KEY`
- Quand c'est Live: `/` -> `{"ok": true}`

## 3) Tester l'API
```bash
# PowerShell
$b = @{ client_id="innerskin"; message="Bonjour" } | ConvertTo-Json -Compress
Invoke-RestMethod -Uri "https://VOTRE-SERVICE.onrender.com/chat" -Method POST -ContentType "application/json" -Body $b
```

## 4) Widget (front)
Ouvre `web/index.html`, remplace `https://REMPLACE-MOI.onrender.com` par l'URL Render.
