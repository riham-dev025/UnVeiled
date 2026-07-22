# main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

# Import models & services
from models import ArticleRequest
from services.nlp_service import get_readability_and_tone
from services.llm_service import extract_dossier_data, analyze_missing_context
from services.search_service import gather_web_context
from services.extractor_service import extract_from_url, extract_from_pdf

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def run_dossier_pipeline(text: str, metadata: dict):
    """Core analysis pipeline shared across raw text, URLs, and PDFs."""
    # 1. Mathematical NLP (VADER & textstat)
    nlp_data = get_readability_and_tone(text)
    
    # 2. Master Brain (Groq Llama 3.1)
    dossier_data = extract_dossier_data(text)
    extracted_claims = dossier_data.get("extracted_claims", [])

    # 3. RAG Search Pipeline
    if extracted_claims:
        web_evidence = gather_web_context(extracted_claims)
        missing_context = analyze_missing_context(text, web_evidence)
    else:
        missing_context = "No specific claims were extracted to verify."

    # 4. Assemble Dossier
    return {
        "status": "success",
        "message": "The Ocular Lens has extracted and verified the metrics.",
        "data": {
            "metadata": metadata,
            "text_preview": text[:100] + "..." if len(text) > 100 else text,
            "objective_summary": dossier_data.get("objective_summary"),
            "extracted_claims": extracted_claims,
            "cited_authorities": dossier_data.get("cited_authorities", []),  # <--- THE MISSING LINK ADDED HERE
            "readability": nlp_data["readability"],
            "emotional_profile": nlp_data["emotional_profile"],
            "persuasive_tactics": dossier_data.get("persuasive_tactics"),
            "missing_context": missing_context
        }
    }


@app.post("/api/analyze")
async def analyze_article(request: ArticleRequest):
    text = ""
    metadata = {
        "title": "Raw Input Text",
        "author": "Unknown / User-Provided",
        "publication_date": "N/A",
        "source_url": "N/A"
    }

    # Resolve URL scraping vs plain text
    if request.url:
        extraction = extract_from_url(request.url)
        if "error" in extraction:
            return {"status": "error", "message": extraction["error"]}
        text = extraction["text"]
        metadata = extraction["metadata"]
    elif request.content:
        text = request.content
    else:
        return {"status": "error", "message": "No text or URL provided."}

    if not text or len(text.strip()) == 0:
        return {"status": "error", "message": "The ink was blank."}

    return run_dossier_pipeline(text, metadata)


@app.post("/api/analyze-pdf")
async def analyze_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return {"status": "error", "message": "The file must be a PDF document."}

    contents = await file.read()
    extraction = extract_from_pdf(contents)

    if "error" in extraction:
        return {"status": "error", "message": extraction["error"]}

    text = extraction["text"]
    metadata = extraction["metadata"]
    metadata["title"] = file.filename

    return run_dossier_pipeline(text, metadata)