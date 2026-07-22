import textstat
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

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