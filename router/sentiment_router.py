from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from transformers import pipeline
import re

# Initialize the sentiment analysis pipeline with truncation and padding
classifier = pipeline(
    "text-classification", 
    model='bhadresh-savani/distilbert-base-uncased-emotion', 
    top_k=None, 
    truncation=True, 
    max_length=512
)

def clean_text(text):
    """Remove HTML tags and extra spaces from the text."""
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    # Remove extra spaces and normalize whitespace
    text = ' '.join(text.split())
    return text

def chunk_text(text, max_length=512):
    """Splits text into chunks of specified max_length (in tokens)."""
    tokens = text.split()  # Assuming space-separated tokens
    for i in range(0, len(tokens), max_length):
        yield ' '.join(tokens[i:i + max_length])

def analyze_sentiment(text):
    """Analyzes sentiment of the given text by processing chunks."""
    sentiment_scores = {'joy': 0, 'anger': 0, 'sadness': 0, 'fear': 0, 'love': 0, 'surprise': 0}
    text = clean_text(text)
    chunks = list(chunk_text(text))

    # Analyze each chunk and aggregate scores
    for chunk in chunks:
        results = classifier(chunk)
        
        # Handle nested list structure
        if results and isinstance(results[0], list):
            results = results[0]  # Unpack the nested list
        
        for result in results:
            if isinstance(result, dict):  # Ensure result is a dictionary
                label = result.get('label', '').lower()
                if label in sentiment_scores:
                    sentiment_scores[label] += result.get('score', 0)
    
    # Average the scores by the number of chunks
    num_chunks = len(chunks)
    if num_chunks > 1:
        sentiment_scores = {k: v / num_chunks for k, v in sentiment_scores.items()}
    
    return sentiment_scores

# Define the router
router = APIRouter()

class SentimentRequest(BaseModel):
    text: str

@router.post("/analyze_sentiment/")
async def analyze_sentiment_endpoint(request: SentimentRequest):
    text = request.text
    try:
        # Perform sentiment analysis
        sentiment_scores = analyze_sentiment(text)
        return {"sentiment": sentiment_scores}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing sentiment: {str(e)}")
