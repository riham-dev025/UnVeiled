import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_dossier_data(text: str):
    """Uses Groq (Llama-3.1) to extract facts, summaries, authorities, and quote-backed persuasion analysis."""
    
    prompt = f"""
    You are TruthLens, an objective information analyst.
    Analyze the text and return ONLY a valid JSON object with no markdown formatting.
    Use this exact structure:
    {{
      "objective_summary": "A calm, neutral 2-sentence summary removing emotional fluff.",
      "extracted_claims": ["claim 1", "claim 2", "claim 3"],
      "cited_authorities": ["Expert/Organization 1", "Expert/Organization 2"],
      "persuasive_tactics": {{
         "Top Tactic Name": "Percentage% - Quote: 'exact sentence from text proving this tactic'",
         "Second Tactic Name": "Percentage% - Quote: 'exact sentence from text proving this tactic'"
      }}
    }}
    
    CRITICAL INSTRUCTIONS:
    1. CITED AUTHORITIES: Extract the names of any experts, medical professionals, organizations, or studies cited in the text (e.g., CDC, FDA, Dr. Smith). If none, return an empty list [].
    2. PERSUASIVE TACTICS: Evaluate for tactics like Fear Appeal, Sensationalism, Loaded Language, Logical Reporting.
    - If the text is objective reporting, the top tactic MUST be "Logical Reporting".
    - You MUST provide an exact quote from the text to justify EVERY score.

    Text: "{text}"
    """
    
    try:
        import json
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
            "cited_authorities": [],
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