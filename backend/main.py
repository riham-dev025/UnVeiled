from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time

app = FastAPI() #API IS ALL CAPITAL!!

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
    time.sleep(2)  #simulation for delay
    return{
        "status":"success",
        "message":"The Occular Lens has processed the ink.",
        "data":{
            "input_recieved": request.content,
            "credibility_score": 43,
            "emotion_detected": "High",
            "missing_context": "The cited study was performed on mice, not humans."
        }
    }