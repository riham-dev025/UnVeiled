import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_dossier_data(text: str):
    """Uses Groq (Llama-3.1) to extract facts, summaries, AND persuasion tactics in one pass."""
    
    prompt = f"""
    You are TruthLens, an objective information analyst.
    Analyze the text and return ONLY a valid JSON object with no markdown formatting.
    Use this exact structure:
    {{
      "objective_summary": "A calm, neutral 2-sentence summary removing emotional fluff.",
      "extracted_claims": ["claim 1", "claim 2", "claim 3"],
      "persuasive_tactics": {{
         "Top Tactic Name (e.g. Sensationalism)": "Percentage (e.g. 85%)",
         "Second Tactic Name (e.g. Fear Appeal)": "Percentage (e.g. 60%)"
      }}
    }}
    
    For persuasive_tactics, evaluate the text and assign a confidence percentage to the top two tactics present. 
    Choose from: Fear Appeal, Sensationalism, Loaded Language, Logical Reporting, Appeal to Authority.

    Text: "{text}"
    """
    
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {
            "objective_summary": "Failed to extract data.",
            "extracted_claims": [],
            "persuasive_tactics": {"error": "The Machine failed to parse the text."},
            "error": str(e)
        }


def analyze_missing_context(original_text: str, web_context: str) -> str:
    """Cross-references the sensational article against live web search results."""
    
    prompt = f"""
    You are TruthLens, an objective fact-checker. 
    Compare the original article with the live web search results.
    Write a concise, 2-3 sentence verdict. 
    State whether the web context supports, debunks, or adds vital missing context to the original article.
    Keep the tone clinical, objective, and neutral. Do not use markdown bolding.

    Original Article: "{original_text}"
    
    Live Web Evidence:
    "{web_context}"
    """
    
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"The Lens was unable to process the web context: {str(e)}"