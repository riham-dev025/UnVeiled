import textstat
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import math
import statistics


# Initialize once to save memory
analyzer = SentimentIntensityAnalyzer()

def get_readability_and_tone(text: str):
    """Calculates reading level and mathematical emotional polarity."""
    
    # Readability
    reading_grade = textstat.flesch_kincaid_grade(text)
    complexity = "High" if reading_grade > 12 else "Standard"
    
    # Emotion
    sentiment_scores = analyzer.polarity_scores(text)
    compound_score = sentiment_scores['compound']
    
    if compound_score >= 0.05:
        primary_tone = "Positive / Favorable"
    elif compound_score <= -0.05:
        primary_tone = "Negative / Critical / Fear-based"
    else:
        primary_tone = "Neutral / Objective"
        
    return {
        "readability": {
            "grade_level": round(reading_grade, 1),
            "complexity": complexity
        },
        "emotional_profile": {
            "primary_tone": primary_tone,
            "raw_scores": sentiment_scores
        }
    }
def estimate_synthetic_ink(text: str) -> dict:
    """Calculates heuristic Perplexity (Entropy) and Burstiness to estimate AI generation."""
    #first, we calculate Burstiness (sentence length variation)
    sentences = re.split(r'[.!?]+',text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 3]

    if len(sentences) < 2:
      return {"burstiness": 0, "perplexity": 0, "verdict": "Insufficient Data"}

    lengths = [len(s.split()) for s in sentences]
    burstiness = statistics.stdev(lengths)
        
    # 2. Calculate Perplexity Approximation (Shannon Entropy)
    words = re.findall(r'\b\w+\b', text.lower())
    word_count = len(words)
    
    if word_count == 0:
        return {"burstiness": 0, "perplexity": 0, "verdict": "Insufficient Data"}
        
    freq_map = {}
    for w in words:
        freq_map[w] = freq_map.get(w, 0) + 1
        
    entropy = 0
    for w, count in freq_map.items():
        p = count / word_count
        entropy -= p * math.log2(p)
        
    # 3. Determine Verdict based on heuristic thresholds
    # AI tends to have lower burstiness (< 5.0) and lower entropy/predictable words.
    verdict = "Human-Authored (High Variance)"
    if burstiness < 5.0 and entropy < 6.5:
        verdict = "Highly Synthetic (Machine-Generated)"
    elif burstiness < 7.0:
        verdict = "Mixed / Heavily Edited"
        
    return {
        "burstiness": round(burstiness, 2),
        "perplexity": round(entropy, 2),
        "verdict": verdict
    }
