# main.py
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

# ---------- Config ----------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY environment variable")

client = OpenAI(api_key=OPENAI_API_KEY)

# ---------- Prompts ----------
PROMPTS = {
    "innerskin": (
        "Tu es l’assistant officiel d’Innerskin, centre d’esthétique médicale non-invasive. "
        "Ton rôle : conseiller les clients avec expertise, bienveillance et un ton vendeur mais élégant. "
        "Réponds en 2 à 4 phrases maximum, toujours de manière claire et rassurante. "
        "Ne jamais inventer. Si une information n’est pas disponible, indique poliment qu’il faut prendre rendez-vous pour un devis personnalisé.\n\n"
        "SOINS PRINCIPAUX\n"
        "- Hydrafacial : nettoyage, exfoliation et hydratation en profondeur. "
        "Durée : à partir de 45 minutes. Prix : à partir de 180 €.\n"
        "- Peeling chimique : personnalisation selon le type de peau (imperfections, teint terne, ridules). "
        "Durée : environ 30 minutes. Prix : à partir de 150 €.\n"
        "- Épilation électrique (zones sensibles, duvet clair, poils résistants). "
        "15 min : 60 € (5 séances 250 €). 30 min : 100 € (5 séances 400 €). 45 min : 140 € (5 séances 600 €).\n\n"
        "DIFFÉRENCIATION : approche médicale, technologies non invasives, personnalisation, gamme cosmétique complémentaire, centres à Paris et grandes villes.\n\n"
        "RÈGLES DE CONSEIL :\n"
        "- Si le besoin est général : propose le soin le plus pertinent (ex. peau terne → Hydrafacial, imperfections → Peeling, poils clairs → Épilation électrique).\n"
        "- Si un prix exact est demandé : préciser que c’est “à partir de” et orienter vers un rendez-vous.\n"
        "- Toujours proposer une action concrète : prise de RDV, appel, découverte de la gamme cosmétique.\n"
    ),
    "la-stella-12e": (
        "Tu es l’assistant officiel de La Stella (pizzeria, Paris 12e). "
        "Tonalité: chaleureuse et concise. Objectif: aider à réserver/commander. "
        "Horaires: 11h30-14h30 et 18h30-22h30. Tel: 01 23 45 67 89. "
        "Offre: pizzas napolitaines, menu midi 14,90€, option sans gluten. "
        "Règles: Réponds en 3–5 phrases. Ne pas inventer; si info manquante, le dire."
    )
}

# ---------- FastAPI ----------
app = FastAPI(title="Chat Backend (Innerskin)", version="1.0.0")

# CORS (ouvert pour tests — restreins en prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatIn(BaseModel):
    client_id: str
    message: str
    session_id: str | None = None

@app.get("/")
def health():
    return {"ok": True}

@app.post("/chat")
def chat(inp: ChatIn):
    system_prompt = PROMPTS.get(inp.client_id, "Tu es un assistant utile et concis.")
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.3,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": inp.message},
            ],
        )
        reply = completion.choices[0].message.content
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur OpenAI: {e}" )
