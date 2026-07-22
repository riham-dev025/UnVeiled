from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import our modularized logic
from models import ArticleRequest
from services.nlp_service import get_readability_and_tone
from services.llm_service import extract_dossier_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/analyze")
async def analyze_article(request: ArticleRequest):
    text = request.content
    
    if not text or len(text.strip()) == 0:
        return {"status": "error", "message": "The ink was blank."}

    # 1. Run local mathematical NLP (VADER & textstat)
    nlp_data = get_readability_and_tone(text)
    
    # 2. Call the Master LLM (Groq)
    dossier_data = extract_dossier_data(text)

    # 3. Assemble the Dossier
    return {
        "status": "success",
        "message": "The Occular Lens has extracted the metrics.",
        "data": {
            "text_preview": text[:50] + "..." if len(text) > 50 else text,
            "objective_summary": dossier_data.get("objective_summary"),
            "extracted_claims": dossier_data.get("extracted_claims"),
            "readability": nlp_data["readability"],
            "emotional_profile": nlp_data["emotional_profile"],
            "persuasive_tactics": dossier_data.get("persuasive_tactics"),
            "missing_context": "Pending Search Engine (Phase 5)"
        }
    }