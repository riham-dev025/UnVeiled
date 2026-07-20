from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import textstat
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline


app = FastAPI() #API IS ALL CAPITAL!!
analyzer = SentimentIntensityAnalyzer()  #initializing the sentiment analyzer when server launches

print("Waking up the NN")
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli") #initializing the zero-shot classifier when server launches
print("The machine is awake now.")

#to allow communication between react and fastapi
#CHANGE THESE when i start in react and deploy
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#defining how incoming data should look 
class ArticleRequest(BaseModel):
    content: str

@app.post("/api/analyze")
async def analyze_article(request: ArticleRequest): #request is the content in ArticleRequest (to access content)
    text = request.content

    #checking is user submitted an empty input
    if not text or len(text.strip()) == 0:
        return {
            "status": "error",
            "message": "The ink was blank. Please provide text."
        }
#The NLP Engine
    reading_grade = textstat.flesch_kincaid_grade(text) #calculating reading grade/complexity
    sentiment_score = analyzer.polarity_scores(text) #calculating sentiment score
    compound_score = sentiment_score["compound"] #extracting compound score from sentiment score

    #translating the score to human language
    if compound_score >= 0.05:
        primary_tone = "Positive"
    elif compound_score <= -0.05:
        primary_tone = "Negative / Critical / Fear-based"
    else:
        primary_tone = "Neutral / Objective"

    #deep learning section
    manipulation_tactics = [
        "fear appeal",
        "sensationalism",
        "logical and objective reporting",
        "loaded language",
        "appeal to authority"
    ]
    tactic_analysis = classifier(text,manipulation_tactics)
    top_tactics = {
        tactic_analysis['labels'][0]: f"{round(tactic_analysis['scores'][0] * 100, 1)}%",
        tactic_analysis['labels'][1]: f"{round(tactic_analysis['scores'][1] * 100, 1)}%"
    }

    return {
        "status": "success",
        "message": "The Occular Lens has extracted the metrics.",
        "data": {
            "text_preview": text[:50] + "..." if len(text) > 50 else text,
            "readability": {
                "grade_level": reading_grade,
                "complexity": "High" if reading_grade > 12 else "Standard"
            },
            "emotional_profile": {
                "primary_tone": primary_tone,
                "raw_scores": sentiment_score
            },
            "persuasive_tactics": top_tactics,
            "missing_context": "Pending Search Engine (Phase 5)"
        }
    }
    